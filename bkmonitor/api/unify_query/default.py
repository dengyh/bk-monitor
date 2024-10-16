# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云 - 监控平台 (BlueKing - Monitor) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import json
import logging
import time

import requests
from django.conf import settings
from rest_framework import serializers
from six.moves.urllib.parse import urljoin

from bkm_space.utils import bk_biz_id_to_space_uid
from bkmonitor.utils.request import get_request
from core.drf_resource import Resource
from core.errors.api import BKAPIError

logger = logging.getLogger("bkmonitor")


class UnifyQueryAPIResource(Resource):
    """
    统一查询模块
    """

    method = ""
    path = ""

    def perform_request(self, params):
        url = urljoin(settings.UNIFY_QUERY_URL, self.path.format(**params))

        request = get_request(peaceful=True)
        if request and hasattr(request, "user"):
            username = request.user.username
        else:
            username = ""

        requests_params = {
            "method": self.method,
            "url": url,
            "headers": {"Bk-Query-Source": f"username:{username}" if username else "backend"},
        }

        if params.get("space_uid"):
            requests_params["headers"]["X-Bk-Scope-Space-Uid"] = params["space_uid"]
        elif params.get("bk_biz_ids"):
            bk_biz_id = params.pop("bk_biz_ids")[0]
            requests_params["headers"]["X-Bk-Scope-Space-Uid"] = bk_biz_id_to_space_uid(bk_biz_id)
        elif request and request.biz_id:
            # request兜底
            requests_params["headers"]["X-Bk-Scope-Space-Uid"] = bk_biz_id_to_space_uid(request.biz_id)

        if self.method in ["PUT", "POST", "PATCH"]:
            requests_params["json"] = params
        elif self.method in ["GET", "HEAD", "DELETE"]:
            requests_params["params"] = params

        r = requests.request(timeout=60, **requests_params)

        result = r.status_code in [200, 204]
        if not result:
            raise BKAPIError(system_name="unify-query", url=url, result=r.text)

        return r.json()


class QueryDataResource(UnifyQueryAPIResource):
    """
    查询数据
    """

    method = "POST"
    path = "/query/ts"

    class RequestSerializer(serializers.Serializer):
        query_list = serializers.ListField()
        metric_merge = serializers.CharField()
        start_time = serializers.CharField()
        end_time = serializers.CharField()
        step = serializers.CharField()
        space_uid = serializers.CharField()
        down_sample_range = serializers.CharField(allow_blank=True)
        timezone = serializers.CharField(required=False)


class QueryDataByPromqlResource(UnifyQueryAPIResource):
    """
    使用PromQL查询数据
    """

    method = "POST"
    path = "/query/ts/promql"

    class RequestSerializer(serializers.Serializer):
        promql = serializers.CharField()
        match = serializers.CharField(default="", allow_blank=True, required=False)
        start = serializers.CharField()
        end = serializers.CharField()
        bk_biz_ids = serializers.ListField(child=serializers.CharField(), allow_empty=True, required=False)
        step = serializers.RegexField(required=False, regex=r"^\d+(ms|s|m|h|d|w|y)$")
        timezone = serializers.CharField(required=False)

        def validate(self, attrs):
            logger.info(f"PROMQL_QUERY: {json.dumps(attrs)}")
            return attrs


class PromqlToStructResource(UnifyQueryAPIResource):
    """
    PromQL转结构化查询参数
    """

    method = "POST"
    path = "/query/ts/promql_to_struct"

    class RequestSerializer(serializers.Serializer):
        promql = serializers.CharField()


class StructToPromqlResource(UnifyQueryAPIResource):
    """
    结构化查询参数转PromQL
    """

    method = "POST"
    path = "/query/ts/struct_to_promql"

    class RequestSerializer(serializers.Serializer):
        query_list = serializers.ListField()
        metric_merge = serializers.CharField(allow_blank=True, required=False)
        order_by = serializers.ListField(allow_null=True, required=False, allow_empty=True)
        step = serializers.CharField(allow_blank=True, required=False, allow_null=True)
        space_uid = serializers.CharField()


class GetDimensionDataResource(UnifyQueryAPIResource):
    """
    获取维度数据
    """

    method = "POST"
    path = "/query/ts/info/{info_type}"

    class RequestSerializer(serializers.Serializer):
        info_type = serializers.CharField(required=True, label="请求资源类型")
        table_id = serializers.CharField(required=False, allow_blank=True)
        conditions = serializers.DictField(required=False, label="查询参数")
        keys = serializers.ListField(required=False)
        limit = serializers.IntegerField(required=False, default=1000)
        metric_name = serializers.CharField(required=False, allow_null=True)
        start_time = serializers.CharField(required=False)
        end_time = serializers.CharField(required=False)


class GetPromqlLabelValuesResource(UnifyQueryAPIResource):
    """
    获取promql label values
    """

    method = "GET"
    path = "/query/ts/label/{label}/values"

    class RequestSerializer(serializers.Serializer):
        match = serializers.ListField(child=serializers.CharField())
        label = serializers.CharField()
        bk_biz_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)

        def validate(self, attrs):
            attrs["match[]"] = attrs.pop("match")
            return attrs


class QueryDataByExemplarResource(QueryDataResource):
    method = "POST"
    path = "/query/ts/exemplar"

    class RequestSerializer(serializers.Serializer):
        query_list = serializers.ListField()
        start_time = serializers.CharField()
        end_time = serializers.CharField()
        down_sample_range = serializers.CharField(allow_blank=True)
        space_uid = serializers.CharField()


class QueryDataByTableResource(UnifyQueryAPIResource):
    method = "POST"
    path = "query/ts/info/time_series"

    class RequestSerializer(serializers.Serializer):
        limit = serializers.IntegerField()
        slimit = serializers.IntegerField()
        metric_name = serializers.CharField(default="")
        table_id = serializers.CharField()
        keys = serializers.ListField(child=serializers.CharField())
        start_time = serializers.CharField()
        end_time = serializers.CharField()
        conditions = serializers.DictField(default={"field_list": [], "condition_list": []})


class GetKubernetesRelationResource(UnifyQueryAPIResource):
    method = "POST"
    path = "/api/v1/relation/multi_resource"

    class RequestSerializer(serializers.Serializer):
        bk_biz_ids = serializers.ListField(child=serializers.IntegerField(), required=True)
        source_info_list = serializers.ListField(child=serializers.DictField(), required=True)

    def validate_request_data(self, request_data):
        request_data = super(GetKubernetesRelationResource, self).validate_request_data(request_data)
        query_list = []
        for source_info in request_data.pop("source_info_list", []):
            data_timestamp = source_info.pop("data_timestamp", int(time.time()))
            query_list.append({"target_type": "system", "timestamp": data_timestamp, "source_info": source_info})
        request_data["query_list"] = query_list
        return request_data
