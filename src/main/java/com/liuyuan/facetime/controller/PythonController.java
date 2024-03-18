package com.liuyuan.facetime.controller;

import com.liuyuan.facetime.model.vo.UserVo;
import com.liuyuan.facetime.service.PythonService;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;


@RestController
@RequestMapping("/user")
public class PythonController {

    /**
     * Python脚本服务
     */
    @Resource
    private PythonService pythonService;

    /**
     * 处理记录用户人脸请求
     *
     * @param userId 用户ID
     * @return 是否记录成功
     */
    @PostMapping("/record/face")
    public Boolean recordFace(Long userId) {
        return pythonService.userRecordFace(userId);
    }

    /**
     * 处理记录用户信息请求
     *
     * @return 是否记录成功
     */
    @PostMapping("/recordInformation")
    public Boolean recordInformation(@RequestBody UserVo userVo) {
        return pythonService.userRecordInformation(userVo.getUserId(),
            userVo.getUserName());
    }

    /**
     * 处理用户签到请求
     *
     * @return 是否签到成功
     */
    @GetMapping("/signIn")
    public Boolean signIn() {
        return pythonService.userSignIn();
    }

    /**
     * 处理记录用户信息请求
     *
     * @return 是否记录成功
     */
    @PostMapping("/recordInformation2")
    public Boolean recordInformation2(@RequestBody UserVo userVo) {
        return pythonService.userRecordInformation2(userVo.getUserId(),
            userVo.getUserName(), userVo.getBase64image());
    }

    /**
     * 处理用户签到请求
     *
     * @return 是否签到成功
     */
    @PostMapping("/signIn2")
    public Boolean signIn2(@RequestBody UserVo userVo) {
        return pythonService.userSignIn2(userVo.getBase64image());
    }
}
