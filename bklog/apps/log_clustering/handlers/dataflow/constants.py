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
from apps.api import BkDataDataFlowApi
from apps.utils import ChoicesEnum
from django.utils.translation import ugettext as _

from apps.log_search.constants import OPERATORS

DEFAULT_TIME_FIELD = "timestamp"
DEFAULT_CLUSTERING_FIELD = "log"
NOT_CLUSTERING_FILTER_RULE = " where ip is null"
OPERATOR_AND = "and"
# 聚类不参与sql字段
NOT_CONTAIN_SQL_FIELD_LIST = ["timestamp", "_startTime_", "_endTime_"]
DIST_FIELDS = ["dist_01", "dist_03", "dist_05", "dist_07", "dist_09"]
RENAME_DIST_FIELDS = ["__dist_01", "__dist_03", "__dist_05", "__dist_07", "__dist_09"]
DIST_CLUSTERING_FIELDS = [
    "dist_01 AS __dist_01",
    "dist_03 AS __dist_03",
    "dist_05 AS __dist_05",
    "dist_07 AS __dist_07",
    "dist_09 AS __dist_09",
]
DEFAULT_SPARK_EXECUTOR_INSTANCES = 8
DEFAULT_SPARK_EXECUTOR_CORES = 2
DEFAULT_SPARK_PSEUDO_SHUFFLE = 200
DEFAULT_SPARK_LOCALITY_WAIT = "0s"

DEFAULT_FLINK_BATCH_SIZE = 100
DEFAULT_FLINK_CPU = 1
DEFAULT_FLINK_MEMORY = 2048
DEFAULT_FLINK_WORKER_NUMS = 2
DEFAULT_FLINK_REPLICAS = 2

STREAM_SOURCE_NODE_TYPE = "stream_source"
DIVERSION_NODE_NAME = _("回流数据")
TSPIDER_STORAGE_NODE_TYPE = "tspider_storage"
TSPIDER_STORAGE_INDEX_FIELDS = ["history_time", "event_time"]
MYSQL_STORAGE_NODE_TYPE = "mysql_storage"

SPLIT_TYPE = "split"


class ActionEnum(object):
    START = "start"
    RESTART = "restart"
    STOP = "stop"


class ActionHandler(object):
    action_handler = {
        ActionEnum.START: BkDataDataFlowApi.start_flow,
        ActionEnum.RESTART: BkDataDataFlowApi.restart_flow,
        ActionEnum.STOP: BkDataDataFlowApi.stop_flow,
    }

    @classmethod
    def get_action_handler(cls, action_num):
        return cls.action_handler.get(action_num, BkDataDataFlowApi.start_flow)


class FlowMode(ChoicesEnum):
    # 预处理flow
    PRE_TREAT_FLOW = "pre_treat_flow"
    # 结果处理flow
    AFTER_TREAT_FLOW = "after_treat_flow"
    # 修改flow的某些节点
    MODIFY_FLOW = "modify_flow"
    # 计算平台rt flow
    AFTER_TREAT_FLOW_BKDATA = "after_treat_flow_bkdata"
    # 在线训练 预测处理 flow
    PREDICT_FLOW = "predict_flow"
    # 在线训练 计算平台 rt flow
    PREDICT_FLOW_BKDATA = "predict_flow_bkdata"
    # 日志数量聚合 flow
    LOG_COUNT_AGGREGATION_FLOW = "log_count_aggregation_flow"

    _choices_labels = (
        (PRE_TREAT_FLOW, "templates/flow/pre_treat_flow.json"),
        (AFTER_TREAT_FLOW, "templates/flow/after_treat_flow.json"),
        (MODIFY_FLOW, "templates/flow/modify_flow.json"),
        (AFTER_TREAT_FLOW_BKDATA, "templates/flow/after_treat_flow_bkdata.json"),
        (PREDICT_FLOW, "templates/flow/predict_flow.json"),
        (PREDICT_FLOW_BKDATA, "templates/flow/predict_flow_bkdata.json"),
        (LOG_COUNT_AGGREGATION_FLOW, "templates/flow/log_count_aggregation_flow.json"),
    )


class NodeType(object):
    REALTIME = "realtime"
    REDIS_KV_SOURCE = "redis_kv_source"
    ELASTIC_STORAGE = "elastic_storage"
    MODEL = "model_ts_custom"
    STREAM_SOURCE = "stream_source"


class RealTimeFlowNode(object):
    PRE_TREAT_NOT_CLUSTERING = "pre_treat_not_clustering"
    PRE_TREAT_SAMPLE_SET = "pre_treat_sample_set"
    AFTER_TREAT_CHANGE_FIELD = "after_treat_change_field"


class RealTimePredictFlowNode(object):
    PREDICT_CLUSTERING = "clustering"
    PREDICT_NOT_CLUSTERING = "not_clustering"
    PREDICT_NODE = "clustering_output"


# 查询字段   __dist_xx
PATTERN_SEARCH_FIELDS = [
    {
      "field_type": "keyword",
      "field_name": field_name,
      "field_alias": "",
      "is_display": False,
      "is_editable": True,
      "tag": "dimension",
      "es_doc_values": True,
      "is_analyzed": False,
      "field_operator": OPERATORS.get("keyword", []),
      "description": None
    } for field_name in RENAME_DIST_FIELDS
]


DEFAULT_MODEL_INPUT_FIELDS = [
    {
        "field_index": 1,
        "data_field_name": "__index__",
        "field_alias": _("系统索引"),
        "components": [],
        "roles": ["system", "index"],
        "data_field_alias": "index",
        "properties": {
            "constraint_type": None,
            "name_inherited": True,
            "value_fixed": False,
            "passthrough": False,
            "role_changeable": False,
            "deletable": False,
            "compatibility": False,
            "extra": {},
            "constraints": {},
            "required": True,
            "complex": False,
        },
        "field_name": "__index__",
        "field_type": "string",
    },
    {
        "field_name": "__id__",
        "field_type": "string",
        "components": ["__group_id__", "timestamp"],
        "field_alias": _("用户索引"),
        "data_field_name": "__id__",
        "data_field_alias": _("用户索引"),
        "roles": ["index"],
        "field_index": 2,
        "properties": {
            "required": True,
            "extra": {},
            "constraint_type": None,
            "compatibility": False,
            "deletable": False,
            "name_inherited": True,
            "complex": True,
            "role_changeable": False,
            "passthrough": False,
            "value_fixed": False,
            "constraints": {},
        },
    },
    {
        "data_field_name": [],
        "data_field_alias": "",
        "field_alias": _("分组字段"),
        "field_type": "string",
        "properties": {
            "name_inherited": True,
            "role_changeable": False,
            "deletable": False,
            "passthrough": False,
            "compatibility": False,
            "complex": False,
            "value_fixed": True,
            "constraints": {},
            "required": True,
            "constraint_type": None,
            "extra": {},
        },
        "roles": ["index_component", "group"],
        "components": [],
        "field_name": "__group_id__",
        "field_index": 3,
    },
    {
        "data_field_name": "log",
        "field_name": "log",
        "field_alias": _("日志内容"),
        "field_type": "string",
        "field_index": 4,
        "data_field_alias": "",
        "components": [],
        "roles": ["passthrough", "feature"],
        "properties": {
            "complex": False,
            "compatibility": False,
            "passthrough": False,
            "required": True,
            "constraint_type": "",
            "role_changeable": False,
            "deletable": False,
            "extra": {},
            "value_fixed": False,
            "name_inherited": False,
            "constraints": {},
        },
    },
    {
        "roles": ["timestamp"],
        "field_index": 5,
        "properties": {
            "constraint_type": "",
            "deletable": False,
            "name_inherited": False,
            "passthrough": False,
            "role_changeable": False,
            "required": True,
            "compatibility": False,
            "constraints": {},
            "extra": {},
            "complex": False,
            "value_fixed": False,
        },
        "field_name": "timestamp",
        "data_field_name": "timestamp",
        "data_field_alias": "",
        "field_alias": _("时间戳"),
        "components": [],
        "field_type": "timestamp",
    },
]


DEFAULT_MODEL_OUTPUT_FIELDS = [
    {
        "data_field_alias": "index",
        "components": [],
        "field_type": "string",
        "properties": {
            "complex": False,
            "constraints": {},
            "extra": {},
            "compatibility": False,
            "constraint_type": None,
            "deletable": False,
            "name_inherited": True,
            "required": True,
            "value_fixed": False,
            "role_changeable": False,
            "passthrough": False,
        },
        "field_alias": _("系统索引"),
        "field_index": 1,
        "roles": ["index"],
        "field_name": "__index__",
        "data_field_name": "__index__",
    },
    {
        "field_alias": _("用户索引"),
        "data_field_alias": _("用户索引"),
        "components": ["__group_id__", "timestamp"],
        "roles": ["index"],
        "properties": {
            "role_changeable": False,
            "name_inherited": True,
            "value_fixed": False,
            "complex": True,
            "deletable": False,
            "passthrough": False,
            "required": True,
            "constraints": {},
            "extra": {},
            "constraint_type": None,
            "compatibility": False,
        },
        "field_name": "__id__",
        "field_index": 2,
        "data_field_name": "__id__",
        "field_type": "string",
    },
    {
        "field_alias": _("分组索引"),
        "roles": ["index_component", "group"],
        "properties": {
            "deletable": False,
            "passthrough": False,
            "complex": False,
            "constraints": {},
            "extra": {},
            "name_inherited": True,
            "compatibility": False,
            "constraint_type": None,
            "role_changeable": False,
            "value_fixed": True,
            "required": True,
        },
        "field_type": "string",
        "field_name": "__group_id__",
        "components": [],
        "field_index": 3,
        "data_field_name": "__group_id__",
        "data_field_alias": _("分组字段"),
    },
    {
        "properties": {
            "name_inherited": False,
            "value_fixed": False,
            "constraint_type": "",
            "deletable": False,
            "extra": {},
            "passthrough": False,
            "compatibility": False,
            "role_changeable": False,
            "required": True,
            "complex": False,
            "constraints": {},
        },
        "field_name": "log_signature",
        "components": [],
        "data_field_name": "",
        "field_alias": "log_signature",
        "field_type": "text",
        "data_field_alias": None,
        "field_index": 5,
        "roles": ["predict_result"],
    },
    {
        "field_name": "timestamp",
        "roles": ["timestamp"],
        "properties": {
            "constraint_type": "",
            "extra": {},
            "compatibility": False,
            "value_fixed": False,
            "passthrough": False,
            "complex": False,
            "role_changeable": False,
            "required": True,
            "constraints": {},
            "deletable": False,
            "name_inherited": True,
        },
        "field_index": 6,
        "data_field_name": "timestamp",
        "components": [],
        "data_field_alias": None,
        "field_type": "timestamp",
        "field_alias": "timestamp",
    },
    {
        "components": [],
        "field_index": 7,
        "properties": {
            "value_fixed": False,
            "required": True,
            "compatibility": False,
            "constraint_type": "",
            "constraints": {},
            "name_inherited": False,
            "role_changeable": False,
            "deletable": False,
            "passthrough": False,
            "complex": False,
            "extra": {},
        },
        "data_field_alias": None,
        "field_type": "string",
        "field_alias": _("日志内容"),
        "roles": ["passthrough", "feature"],
        "data_field_name": "log",
        "field_name": "log",
    },
    {
        "used_by": "user",
        "components": [],
        "field_alias": "pattern",
        "data_field_alias": "",
        "allowed_values": [],
        "roles": ["predict_result"],
        "origin": [],
        "field_container_type": "undefined",
        "output_mark": True,
        "autoPassthrough": False,
        "field_name": "pattern",
        "field_index": 8,
        "data_field_name": "",
        "field_type": "text",
        "description": None,
        "data_field_type": "",
        "default_value": "",
        "sample_value": None,
        "value": "",
        "properties": {
            "value_fixed": False,
            "constraint": [],
            "constraints": {},
            "extra": {},
            "condition": {},
            "role_changeable": False,
            "name_inherited": False,
            "complex": False,
            "passthrough": False,
            "compatibility": False,
            "anonymous": False,
            "label_rules": {"type": "enum", "enum_list": []},
            "deletable": False,
            "is_required": True,
            "constraint_type": "",
        },
    },
    {
        "default_value": "",
        "sample_value": None,
        "value": "",
        "data_field_alias": "",
        "roles": ["predict_result"],
        "origin": [],
        "description": None,
        "used_by": "user",
        "field_index": 9,
        "data_field_name": "",
        "allowed_values": [],
        "autoPassthrough": False,
        "field_name": "is_new",
        "field_alias": "is_new",
        "components": [],
        "field_type": "int",
        "properties": {
            "is_required": True,
            "constraint_type": "",
            "deletable": False,
            "name_inherited": False,
            "complex": False,
            "anonymous": False,
            "role_changeable": False,
            "passthrough": False,
            "constraint": [],
            "value_fixed": False,
            "compatibility": False,
            "condition": {},
            "label_rules": {"type": "enum", "enum_list": []},
            "constraints": {},
            "extra": {},
        },
        "field_container_type": "undefined",
        "output_mark": True,
        "data_field_type": "",
    },
]


class OperatorOnlineTaskEnum(object):
    CREATE = "create"
    UPDATE = "update"


class OnlineTaskTrainingArgs(object):
    IS_NEW = "1"
    USE_OFFLINE_MODEL = 0
    ST_LIST = "0.9,0.8875,0.875,0.8625,0.85"
