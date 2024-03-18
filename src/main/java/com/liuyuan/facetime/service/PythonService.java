package com.liuyuan.facetime.service;

import java.io.Serializable;

/**
 * @author liuyuan-1024
 */
public interface PythonService {

    /**
     * 存储临时图片
     *
     * @param imageCode 前端传入的image的base64编码
     * @return image地址
     */
    String saveImage(String imageCode);


    /**
     * 生成运行python文件的脚本.
     * 注意: 将anaconda加入系统环境变量, 否则会报错
     *
     * @param condaEnv      anaconda的虚拟环境名称
     * @param rootDirectory python项目根目录, python项目默认放到resources目录
     * @param fileName      文件名称, 需要携带后缀名, 脚本文件默认放到python项目
     *                      根目录下, 层级不深方便调用.
     * @param parameters    python脚本的参数, 可传入多个
     * @return 脚本命令
     */
    String generateScript(String condaEnv, String rootDirectory,
                          String fileName, String... parameters);

    /**
     * 调用cmd运行指定的脚本命令.
     *
     * @param script 脚本命令
     * @return 脚本执行结果
     */
    String runScript(String script);

    /**
     * 记录用户人脸.
     *
     * @param id 用户ID
     * @return 是否记录成功
     */
    Boolean userRecordFace(Serializable id);

    /**
     * 记录个人信息并存入数据库
     *
     * @return 是否成功录入用户信息
     */
    Boolean userRecordInformation(Long id, String name);

    /**
     * 用户签到.
     *
     * @return 是否签到成功
     */
    Boolean userSignIn();

    /**
     * 记录用户人脸.
     *
     * @param id        用户ID
     * @param imageCode 图片base64编码
     * @return 是否记录成功
     */
    Boolean userRecordFace2(Serializable id, String imageCode);

    /**
     * 记录个人信息并存入数据库
     *
     * @return 是否成功录入用户信息
     */
    Boolean userRecordInformation2(Long id, String name, String imageCode);

    /**
     * 用户签到2.
     *
     * @return 是否签到成功
     */
    Boolean userSignIn2(String imageCode);
}
