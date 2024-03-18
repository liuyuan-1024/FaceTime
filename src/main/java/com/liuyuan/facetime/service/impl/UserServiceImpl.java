package com.liuyuan.facetime.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.liuyuan.facetime.model.entity.User;
import com.liuyuan.facetime.service.UserService;
import com.liuyuan.facetime.mapper.UserMapper;
import org.springframework.stereotype.Service;

/**
* @author 源
* @description 针对表【user(用户表)】的数据库操作Service实现
* @createDate 2023-06-07 23:41:55
*/
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User>
    implements UserService{

}




