###登录验证接口
+ 请求路径：login
+ 请求方法：post
+ 请求参数

| 参数名    | 参数说明 | 备注     |
| --------- | -------- | -------- |
| user_name | 用户名   | 不能为空 |
| user_pwd  | 密码     | 不能为空 |

- 响应参数

| 参数名    | 参数说明 | 备注            |
| --------- | -------- | --------------- |
| token     | 令牌     | 基于 jwt 的令牌 |
| user_id   | 用户id   |                 |
| user_name | 用户名   |                 |

+ 响应数据

```json

{
    "code": 1000,
    "data": {
        "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTYyNTI5OTAzOCwiZXhwIjoxNjI1Mzg1NDM4fQ.eyJ1c2VyX2lkIjoxLCJ1c2VyX25hbWUiOiJjcyJ9.vvdv4enUx5NwUXjX0E4gUbjlQxf2vC1TvHbLzRdgiuQHC9IbQjiND7_gTN6atbWet5hyDKddXWMYAMJ_K3d3rA",
        "user_id": 1,
        "user_name": "cs"
    },
    "msg": "登录成功"
}
```