| 资源名称 |  资源类型   |   资源链接    |       支持方法        |                                                属性名称                                                 |  关联属性  | 备注 |
| ------ | --------- | ----------- | ------------------- | ----------------------------------------------------------------------------------------------------- | -------- | -- |
| ai 能力  |     api     |     /apis     | get/post/patch/delete |                    name/category_code/dri/outline/features/banner_images_url/doc_url                    |   invoke   |      |
| 能力分类 |  category   |  /categories  | get/post/patch/delete |                                            name/code/outline                                            |    apis    |      |
| 能力调用 |   invoke    |   /invokes    | get/post/patch/delete |                                              url/protocol                                               | parameters |      |
| 调用参数 |  parameter  |  /parameters  | get/post/patch/delete |                         name/data_type/is_required/desc/example/parameter_type                          |   invoke   |      |
| 应用信息 | application | /applications | get/post/patch/delete |                                  name/type/app_key/app_secret/desc/dri                                  |   apiss    |      |
| 能力申请 |    apply    |   /applies    | get/post/patch/delete | api_id/application_id/dri/apply_datetime/approval_result/approval_reason/approval_dri/approval_datetime |            |      |
| 字典信息 |    dict     |    /dicts     | get/post/patch/delete |                                       name/code/parent_id/remark                                        |  children  |      |
