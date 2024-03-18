use facetime;

-- 用户表
create table if not exists `user`
(
    `id`           bigint                               not null
        auto_increment comment '用户ID',
    `name`         varchar(256)                         not null
        comment '用户姓名',
    `sign_in_time` datetime                             null
        comment '用户签到时间',
    `created_at`   datetime   default CURRENT_TIMESTAMP not null
        comment '创建时间',
    `updated_at`   datetime   default CURRENT_TIMESTAMP not null on update
                CURRENT_TIMESTAMP comment '最后更新时间',
    `is_deleted`   tinyint(1) default 0                 not null
        comment '是否已删除(0-未删除 1-已删除)',
    primary key (`id`)
) comment '用户表'
    engine = InnoDB
    default charset = utf8mb4
    collate = utf8mb4_unicode_ci;