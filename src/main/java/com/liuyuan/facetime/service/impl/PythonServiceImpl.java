package com.liuyuan.facetime.service.impl;

import com.baomidou.mybatisplus.core.conditions.update.LambdaUpdateWrapper;
import com.baomidou.mybatisplus.core.toolkit.ObjectUtils;
import com.liuyuan.facetime.model.entity.User;
import com.liuyuan.facetime.service.PythonService;
import com.liuyuan.facetime.service.UserService;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.nio.charset.Charset;
import java.util.Base64;
import java.util.Date;
import java.util.Objects;


@Service
public class PythonServiceImpl implements PythonService {

    private final String defaultEnv = "FaceRecognition";
    private final String defaultRootDirectory = "insightface_pytorch";

    @Resource
    private UserService userService;

    @Override
    public String saveImage(String imageCode) {
        // rootDirectory在输出目录中的路径
        String targetPath = Objects.requireNonNull(PythonServiceImpl.class
            .getClassLoader().getResource("insightface_pytorch")).getPath();
        // 转成 rootDirectory在源代码目录中的路径
        String srcPath = new File(targetPath).getParentFile().getParentFile()
            .getParentFile().getPath();
        // 资源目录路径
        String resourcesPath = srcPath + "\\src\\main\\resources\\";
        // rootDirectory绝对路径
        String rootPath = resourcesPath + "insightface_pytorch\\data\\temp\\";
        // 解码后的图片的存储位置
        String imagePath = rootPath + "out.jpg";
        // 新建文件，随后将图片写入此文件
        File outputFile = new File(imagePath);

        try {
            // base64解码
            byte[] imageBytes = Base64.getDecoder().decode(imageCode);
            // 转成图片
            BufferedImage img =
                ImageIO.read(new ByteArrayInputStream(imageBytes));
            ImageIO.write(img, "jpg", outputFile);
            // 返回解码后的图片的存储位置
            return imagePath;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public String generateScript(String env, String rootDirectory,
                                 String fileName, String... parameters) {
        // rootDirectory在输出目录中的路径
        String targetPath = Objects.requireNonNull(PythonServiceImpl.class
            .getClassLoader().getResource(rootDirectory)).getPath();
        // 转成 rootDirectory在源代码目录中的路径
        String srcPath = new File(targetPath).getParentFile().getParentFile()
            .getParentFile().getPath();
        // 资源目录路径
        String resourcesPath = srcPath + "\\src\\main\\resources\\";
        // rootDirectory绝对路径
        String rootPath = resourcesPath + rootDirectory;
        // 生成脚本雏形
        StringBuilder script = new StringBuilder("cd /d " + rootPath
            + " && activate " + env + " && python " + fileName);
        // 添加脚本参数
        for (String para : parameters) {
            script.append(" ").append(para);
        }

        return script.toString();
    }

    @Override
    public String runScript(String script) {
        StringBuilder result = new StringBuilder();

        try {
            ProcessBuilder builder = new ProcessBuilder("cmd.exe",
                "/c", script);

            Process process = builder.start();
            int exitCode = process.waitFor();
            if (exitCode == 0) {
                // 获取输入流Reader,并转码为GBK
                InputStream inputStream = process.getInputStream();
                BufferedReader inputReader = new BufferedReader(
                    new InputStreamReader(inputStream, Charset.forName("GBK")));
                // 打印输入流信息
                String inputLine;
                while ((inputLine = inputReader.readLine()) != null) {
                    result.append(inputLine);
                }
            } else {
                InputStream errorStream = process.getErrorStream();
                BufferedReader errorReader = new BufferedReader(
                    new InputStreamReader(errorStream, Charset.forName("GBK")));
                // 打印输入流信息
                String errorLine;
                while ((errorLine = errorReader.readLine()) != null) {
                    result.append(errorLine);
                }
            }
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException(e);
        }

        return result.toString();
    }

    @Override
    public Boolean userRecordFace(Serializable id) {
        String fileName = "record_face.py";
        String[] parameters = new String[]{"-n "};
        parameters[0] += id;

        String script = this.generateScript(
            defaultEnv, defaultRootDirectory, fileName, parameters);

        String result = this.runScript(script);

        return Integer.parseInt(result) == 0;
    }

    @Override
    public Boolean userRecordInformation(Long id, String name) {
        if (ObjectUtils.isNotEmpty(userService.getById(id))) {
            return false;
        }

        // 录入人脸
        Boolean result = this.userRecordFace(id);

        if (result) {
            User user = new User();
            user.setId(id);
            user.setName(name);
            userService.save(user);
            return true;
        }

        return false;
    }

    @Override
    public Boolean userSignIn() {
        String filePath = "sign_in.py";

        String script = this.generateScript(
            defaultEnv, defaultRootDirectory, filePath);

        String id = this.runScript(script);

        // id小于0, 这是异常情况
        if (id.compareTo("0") < 0) {
            return false;
        }

        User user = userService.getById(id);

        if (ObjectUtils.isEmpty(user)) {
            throw new RuntimeException("查无此人");
        }

        LambdaUpdateWrapper<User> wrapper = new LambdaUpdateWrapper<>();
        wrapper.eq(User::getId, id).set(User::getSignInTime, new Date());
        userService.update(wrapper);
        return true;
    }

    @Override
    public Boolean userRecordFace2(Serializable id, String imageCode) {
        String imagePath = this.saveImage(imageCode);

        String fileName = "record_face2.py";
        String[] parameters = new String[]{"-n ", "-i "};
        parameters[0] += id;
        parameters[1] += imagePath;

        String script = this.generateScript(defaultEnv, defaultRootDirectory,
            fileName, parameters);

        String result = this.runScript(script);
        return Integer.parseInt(result) == 0;
    }

    @Override
    public Boolean userRecordInformation2(Long id, String name,
                                          String imageCode) {
        User user = userService.getById(id);

        if (ObjectUtils.isNotEmpty(user)) {
            // 用户已存在, 更新用户人脸信息
            return this.userRecordFace2(id, imageCode);
        }

        // 用户不存在, 录入人脸并存入数据库
        Boolean result = this.userRecordFace2(id, imageCode);
        if (result) {
            user = new User();
            user.setId(id);
            user.setName(name);
            userService.save(user);
            return true;
        }
        return false;
    }

    @Override
    public Boolean userSignIn2(String imageCode) {
        String imagePath = this.saveImage(imageCode);

        String filePath = "sign_in2.py";
        String para = "-i " + imagePath;

        String script = this.generateScript(
            defaultEnv, defaultRootDirectory, filePath, para);

        String id = this.runScript(script);

        // id小于0, 这是异常情况
        if (id.compareTo("0") < 0) {
            return false;
        }

        User user = userService.getById(id);

        if (ObjectUtils.isEmpty(user)) {
            throw new RuntimeException("查无此人");
        }

        LambdaUpdateWrapper<User> wrapper = new LambdaUpdateWrapper<>();
        wrapper.eq(User::getId, id).set(User::getSignInTime, new Date());
        userService.update(wrapper);
        return true;
    }
}
