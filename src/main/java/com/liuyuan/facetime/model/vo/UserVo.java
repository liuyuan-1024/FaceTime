package com.liuyuan.facetime.model.vo;

import lombok.Data;

import java.io.Serializable;
import java.util.Date;

/**
 * @author liuyuan-1024
 */
@Data
public class UserVo implements Serializable {
    private static final long serialVersionUID = 1L;

    /**
     * 用户ID
     */
    private Long userId;

    /**
     * 用户姓名
     */
    private String userName;

    /**
     * 用户签到时间
     */
    private Date signInTime;

    /**
     * 用户人脸图片
     */
    private String base64image;
}
