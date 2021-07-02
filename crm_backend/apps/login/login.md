###登录验证接口
+ 请求路径：login
+ 请求方法：post
+ 请求参数

| 参数名    | 参数说明 | 备注     |
| --------- | -------- | -------- |
| user_name | 用户名   | 不能为空 |
| user_pwd  | 密码     | 不能为空 |

- 响应参数

| 参数名 | 参数说明 | 备注            |
| ------ | -------- | --------------- |
| token  | 令牌     | 基于 jwt 的令牌 |

+ 响应数据

```json
{
    "code": 1000,
    "data": {
        "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTYyNTI0NjQzMiwiZXhwIjoxNjI1MzMyODMyfQ.eyJ1c2VyX2lkIjoxLCJ1c2VyX25hbWUiOiJjcyJ9.OATtYAGEcBnCyy1nmgfejbr2M4D4KXThAgn4jqtpLML9TJVzcCFhiB-eTSA4fmw6IvAgxkMq_B4SLH8HUZMzmA"
    },
    "msg": "登录成功"
}
```