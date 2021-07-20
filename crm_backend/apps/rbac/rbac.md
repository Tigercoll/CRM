## 左侧菜单栏

+ 请求路径：menu
+ 请求方法：get
+ 响应数据

```json
{
    "code": 1000,
    "data": [
        {
            "id": 1,
            "permission_name": "用户管理",
            "permission_url": "users",
            "permission_level": 1,
            "permission_parent_id": null,
            "children": [
                {
                    "id": 2,
                    "permission_name": "用户列表",
                    "permission_url": "users",
                    "permission_level": 2,
                    "permission_parent_id": 1
                }
            ]
        }
    ],
    "msg": "获取菜单列表"
}
```

