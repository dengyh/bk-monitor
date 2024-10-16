# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making BK-LOG 蓝鲸日志平台 available.
Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.
BK-LOG 蓝鲸日志平台 is licensed under the MIT License.
License for BK-LOG 蓝鲸日志平台:
--------------------------------------------------------------------
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
We undertake not to change the open source license (MIT license) applicable to the current version of
the project delivered to anyone in the future.
"""
from apps.generic import ModelViewSet
from apps.log_desensitize.handlers.desensitize import DesensitizeRuleHandler
from apps.log_desensitize.models import DesensitizeRule

from rest_framework.response import Response

from apps.log_desensitize.serializers import DesensitizeRuleSerializer, DesensitizeRuleListSerializer


class DesensitizeRuleViesSet(ModelViewSet):
    """
    脱敏规则
    """
    lookup_field = "id"
    model = DesensitizeRule

    def get_permissions(self):
        return []

    def list(self, request, *args, **kwargs):
        """
        @api {GET} /api/v1/desensitize/rule/?space_uid=$space_uid&is_public=$is_public 脱敏规则列表
        @apiName desensitize_rule list
        @apiGroup DesensitizeRule
        @apiSuccess {String} rule_name 脱敏规则名称
        @apiSuccess {Array} match_fields 匹配的字段名列表
        @apiSuccess {String} match_pattern 匹配表达式
        @apiSuccess {String} operator 脱敏算子 可选字段 ‘mask_shield, text_replace’
        @apiSuccess {Json} operator_params 脱敏算子参数
        @apiSuccess {Int} operator_params.preserve_head 掩码屏蔽算子参数 保留前几位  默认 0
        @apiSuccess {Int} operator_params.preserve_tail 掩码屏蔽算子参数 保留后几位  默认 0
        @apiSuccess {String} operator_params.replace_mark 掩码屏蔽算子参数 替换符号 默认 *
        @apiSuccess {String} operator_params.template_string 文本替换算子参数 替换模板
        @apiSuccess {Bool} is_active 是否启用
        @apiSuccess {Bool} is_public 是否全局规则
        @apiSuccess {Int} access_num 接入项总数
        @apiSuccess {Array} access_info 接入项
        @apiSuccess {String} access_info.scenario_id 接入场景
        @apiSuccess {String} access_info.scenario_name 接入场景名称
        @apiSuccess {Array} access_info.ids 接入场景ID列表
        @apiParamapiSuccess {Json} 返回示例:
        {
            "message": "",
            "code": 0,
            "data": [
                {
                    "id": 1,
                    "rule_name": "测试脱敏规则1"，
                    "match_fields": ["phone", "number"]
                    "match_pattern": "\\d+",
                    "operator": "mask_shield",
                    "operator_params": {
                        "preserve_head": 1,
                        "preserve_tail": 2,
                        "replace_mark": "*"
                    },
                   "is_active": true,
                   "is_public": false,
                   "access_num": 4439,
                   "access_info": [
                        {
                            "scenario_id": "log",
                            "scenario_name": "采集接入",
                            "ids": [1,2,3]
                        },
                        {
                            "scenario_id": "log",
                            "scenario_name": "自定义上报",
                            "ids": [4,5,6]
                        },
                        {
                            "scenario_id": "bkdata",
                            "scenario_name": "数据平台",
                            "ids": [7,8,9]
                        },
                        {
                            "scenario_id": "es",
                            "scenario_name": "第三方ES",
                            "ids": [10,11,12]
                        }
                    ]
                }
            ],
            "result": true
        }
        """
        data = self.params_valid(DesensitizeRuleListSerializer)
        return Response(DesensitizeRuleHandler().list(is_public=data["is_public"], space_uid=data["space_uid"]))

    def create(self, request, *args, **kwargs):
        """
        @api {POST} /api/v1/desensitize/rule/ 创建脱敏规则
        @apiName desensitize_rule create
        @apiGroup DesensitizeRule
        @apiParam {String} space_uid 空间唯一标识
        @apiParam {String} rule_name 脱敏规则名称
        @apiParam {Array} match_fields 匹配的字段名列表
        @apiParam {String} match_pattern 匹配表达式
        @apiParam {String} operator 脱敏算子 可选字段 ‘mask_shield, text_replace’
        @apiParam {Json} operator_params 脱敏算子参数
        @apiParam {Int} operator_params.preserve_head 掩码屏蔽算子参数 保留前几位  默认 0
        @apiParam {Int} operator_params.preserve_tail 掩码屏蔽算子参数 保留后几位  默认 0
        @apiParam {String} operator_params.replace_mark 掩码屏蔽算子参数 替换符号 默认 *
        @apiParam {String} operator_params.template_string 文本替换算子参数 替换模板
        @apiParam {Bool} is_public 是否为全局规则
        @apiParamExample {Json} 请求示例:
        {
            "space_uid": "bkcc__2",
            "rule_name": "测试脱敏规则",
            "match_fields": ["phone", "number"],
            "match_pattern": "\\d+",
            "operator": "mask_shield",
            "operator_params": {
                "preserve_head": 1,
                "preserve_tail": 2,
                "replace_mark": "*"
            },
            "is_public": false
        }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "code": 0,
            "data": {
                "id": 1
            },
            "result": true
        }
        """
        data = self.params_valid(DesensitizeRuleSerializer)
        return Response(DesensitizeRuleHandler().create_or_update(params=data))

    def update(self, request, *args, id=None, **kwargs):
        """
        @api {PUT} /api/v1/desensitize/rule/$rule_id/ 创建脱敏规则
        @apiName desensitize_rule update
        @apiGroup DesensitizeRule
        @apiParam {String} rule_name 脱敏规则名称
        @apiParam {Array} match_fields 匹配的字段名列表
        @apiParam {String} match_pattern 匹配表达式
        @apiParam {String} operator 脱敏算子 可选字段 ‘mask_shield, text_replace’
        @apiParam {Json} operator_params 脱敏算子参数
        @apiParam {Int} operator_params.preserve_head 掩码屏蔽算子参数 保留前几位  默认 0
        @apiParam {Int} operator_params.preserve_tail 掩码屏蔽算子参数 保留后几位  默认 0
        @apiParam {String} operator_params.replace_mark 掩码屏蔽算子参数 替换符号 默认 *
        @apiParam {String} operator_params.template_string 文本替换算子参数 替换模板
        @apiParamExample {Json} 请求示例:
        {
            "rule_name": "测试脱敏规则",
            "match_fields": ["phone", "number"],
            "match_pattern": "\\d+",
            "operator": "mask_shield",
            "operator_params": {
                "preserve_head": 1,
                "preserve_tail": 2,
                "replace_mark": "*"
            }
        }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "code": 0,
            "data": {
                "id": 1
            },
            "result": true
        }
        """
        data = self.params_valid(DesensitizeRuleSerializer)
        return Response(DesensitizeRuleHandler(rule_id=int(id)).create_or_update(params=data))

    def retrieve(self, request, *args, id=None, **kwargs):
        """
        @api {GET} /api/v1/desensitize/rule/{$rule_id}/ 脱敏规则详情
        @apiName desensitize_rule retrieve
        @apiGroup DesensitizeRule
        @apiParam {Int} rule_id 脱敏规则ID
        @apiSuccess {String} rule_name 脱敏规则名称
        @apiSuccess {Array} match_fields 匹配的字段名列表
        @apiSuccess {String} match_pattern 匹配表达式
        @apiSuccess {String} operator 脱敏算子 可选字段 ‘mask_shield, text_replace’
        @apiSuccess {Json} operator_params 脱敏算子参数
        @apiSuccess {Int} operator_params.preserve_head 掩码屏蔽算子参数 保留前几位  默认 0
        @apiSuccess {Int} operator_params.preserve_tail 掩码屏蔽算子参数 保留后几位  默认 0
        @apiSuccess {String} operator_params.replace_mark 掩码屏蔽算子参数 替换符号 默认 *
        @apiSuccess {String} operator_params.template_string 文本替换算子参数 替换模板
        @apiParamapiSuccess {Json} 返回示例:
        {
            "message": "",
            "code": 0,
            "data": {
                "rule_name": "测试脱敏规则"，
                "match_fields": ["phone", "number"]
                "match_pattern": "\\d+",
                "operator": "mask_shield",
                "operator_params": {
                    "preserve_head": 1,
                    "preserve_tail": 2,
                    "replace_mark": "*"
                }
            },
            "result": true
        }
        """
        return Response(DesensitizeRuleHandler(rule_id=int(id)).retrieve())

    def destroy(self, request, *args, id=None, **kwargs):
        """
        @api {DELETE} /api/v1/desensitize/rule/{$rule_id}/ 删除脱敏规则
        @apiName desensitize_rule delete
        @apiGroup DesensitizeRule
        @apiSuccessExample {json} 成功返回:
        {
            "result": true,
            "data": null,
            "code": 0,
            "message": ""
        }
        """
        return Response(DesensitizeRuleHandler(rule_id=int(id)).destroy())
