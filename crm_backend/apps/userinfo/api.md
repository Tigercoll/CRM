## 用户管理接口

### 获取用户列表

+ 请求路径:users/?page=1&&size=10
+ 请求方法:get
+ 查询参数

| 参数名 | 参数说明 | 备注     |
| ------ | -------- | -------- |
| page   | 页数     | 可以为空 |
| size   | 分页长度 | 可以为空 |

+ 响应数据

```json
{
  "code": 1000,
  "data": {
    "user_list": [
      {
        "id": 1,
        "user_name": "2",
        "user_email": "3",
        "create_time": "2021-07-04T08:44:27.301000",
        "user_status": {
          "id": 1,
          "status": "启用"
        }
      },
      {
        "id": 2,
        "user_name": "33",
        "user_email": "123@qq.com",
        "create_time": "2021-07-11T12:12:42",
        "user_status": {
          "id": 1,
          "status": "启用"
        }
      }
    ],
    "total": 2,
    "current_page": 1
  },
  "msg": "获取用户列表成功"
}
```

### 添加用户

+ 请求路径:users/
+ 请求方法:post
+ 请求参数

| 参数名     | 参数说明 | 备注     |
| ---------- | -------- | -------- |
| user_name  | 用户名   | 不能为空 |
| user_pwd   | 密码     | 不能为空 |
| user_pwd_r | 确认密码 | 不能为空 |
| user_email | 邮箱     | 不能为空 |

+ 响应数据

```json
{
  "code": 1000,
  "data": "",
  "msg": "用户添加成功"
}
```

### 修改用户

+ 请求路径:`users/${id}`
+ 请求方法:put
+ 请求参数

| 参数名      | 参数说明 | 备注                                      |
| ----------- | -------- | ----------------------------------------- |
| id          | id       | 路径参数，不能为空                        |
| user_name   | 用户名   | 可以为空                                  |
| user_pwd    | 密码     | 可以为空                                  |
| user_email  | 邮箱     | 可以为空                                  |
| user_status | 用户状态 | 可以为空，为int类型，从status_list 中选取 |
| roles_id    | 角色id   | 可以为空，为数组类型，从roles_list中选取  |

+ 响应结果

```json
{
    "code":1000,
    "data":{
        "id":1,
        "user_name":"cs",
        "user_pwd":"123",
        "user_email":"123@qq.com",
        "user_status":2,
        "roles_id":[
            1,
            3
        ],
        "status_list":[
            [
                1,
                "启用"
            ],
            [
                2,
                "删除"
            ]
        ],
        "roles_list":[
            {
                "id":1,
                "role_name":"老师",
                "role_desc":"老师"
            },
            {
                "id":3,
                "role_name":"管理员",
                "role_desc":"管理员"
            }
        ]
    },
    "msg":"修改成功"
}
```

### 删除用户

+ 请求路径:`users/${id}`
+ 请求方法:delete
+ 响应结果

```json
{"code":1000,"data":"","msg":"删除成功"}
```































