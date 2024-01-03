/*
 * Tencent is pleased to support the open source community by making
 * 蓝鲸智云PaaS平台 (BlueKing PaaS) available.
 *
 * Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.
 *
 * 蓝鲸智云PaaS平台 (BlueKing PaaS) is licensed under the MIT License.
 *
 * License for 蓝鲸智云PaaS平台 (BlueKing PaaS):
 *
 * ---------------------------------------------------
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
 * to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of
 * the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
 * THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
 * CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */
import { Component, Prop, Watch } from 'vue-property-decorator';
import { Component as tsc } from 'vue-tsx-support';

import { random } from '../../../../../monitor-common/utils';
import MetricSelector from '../../../../components/metric-selector/metric-selector';
import { IScenarioItem, MetricDetail, MetricType } from '../typings';

import './aiops-monitor-metric-select.scss';

interface IProps {
  value?: string[];
  metrics?: MetricDetail[];
  scenarioList?: IScenarioItem[];
  defaultScenario?: string;
  onChange?: (v: string[]) => void;
}

@Component
export default class AiopsMonitorMetricSelect extends tsc<IProps> {
  @Prop({ type: Array, default: () => [] }) value: string[];
  @Prop({ type: Array, default: () => [] }) metrics: MetricDetail[];
  @Prop({ type: Array, default: () => [] }) scenarioList: IScenarioItem[];
  /* 默认选择的监控对象 */
  @Prop({ type: String, default: '' }) defaultScenario: string;

  localValue = [];
  tags: MetricDetail[] = [];

  showSelector = false;
  selectTargetId = '';

  showAll = false;

  created() {
    this.selectTargetId = `aiops-monitor-metric-select-component-id-${random(8)}`;
  }

  @Watch('value', { immediate: true })
  handleWatchValue(value: string[]) {
    if (JSON.stringify(value) !== JSON.stringify(this.localValue)) {
      this.localValue = this.value;
      this.handleGetMetricTag();
    }
  }
  @Watch('metrics', { immediate: true })
  handleWatchMetrics(value) {
    if (value.length) {
      this.handleGetMetricTag();
    }
  }

  /**
   * @description 获取tag数据
   */
  handleGetMetricTag() {
    const metricMap = new Map();
    this.metrics.forEach(item => {
      metricMap.set(item.metric_id, item);
    });
    const tags = [];
    this.localValue.forEach(id => {
      const metric = metricMap.get(id);
      if (metric) {
        tags.push(metric);
      }
    });
    this.tags = tags;
    this.$nextTick(() => {
      this.getOverflowHideCount();
    });
  }
  /**
   * @description 点击当前组件
   */
  handleClick() {
    this.showAll = !this.showAll;
    this.$nextTick(() => {
      this.getOverflowHideCount();
      if (this.showAll) {
        this.showSelector = true;
      }
    });
  }

  /**
   * @description 获取隐藏的数据
   */
  getOverflowHideCount() {
    const tagsWrap = this.$el.querySelector('.tag-select-wrap');
    const countClassName = 'overflow-count';
    const dels = tagsWrap.querySelectorAll(`.${countClassName}`);
    dels.forEach(el => {
      el.parentNode.removeChild(el);
    });
    if (this.showAll) {
      return;
    }
    const tagsEl = tagsWrap.querySelectorAll('.tag-item');
    if ((tagsWrap as any).offsetHeight < (this.$el as any).offsetHeight) {
      return;
    }
    // 容器宽度
    const wrapWidth = (this.$el as any).offsetWidth - 24;
    // 隐藏的数量tag宽度
    const countWrapWidth = 36;
    let countWidth = 0;
    let overflowCount = 0;
    let insertIndex = 0;
    for (let i = 0; i < tagsEl.length; i++) {
      const width = (tagsEl[i] as any).offsetWidth;
      countWidth += width + 4;
      console.log(countWidth, wrapWidth, countWrapWidth);
      if (countWidth > wrapWidth - countWrapWidth && countWidth !== wrapWidth) {
        if (!insertIndex) {
          insertIndex = i;
        }
        overflowCount += 1;
      }
    }
    if (overflowCount) {
      const countEl = document.createElement('span');
      countEl.className = countClassName;
      countEl.innerHTML = `+${overflowCount}`;
      tagsWrap.insertBefore(countEl, tagsWrap.children[insertIndex]);
    }
  }

  /**
   * @description 展示指标选择器
   * @param v
   */
  handleShowSelector(v: boolean) {
    this.showSelector = v;
    if (!v) {
      this.showAll = false;
      this.$nextTick(() => {
        this.getOverflowHideCount();
      });
    }
  }
  /**
   * @description 删除
   * @param event
   * @param index
   */
  handleDel(event: Event, index: number) {
    event.stopPropagation();
    this.tags.splice(index, 1);
    this.handleChange();
    this.$nextTick(() => {
      this.getOverflowHideCount();
    });
  }

  handleChange() {
    this.localValue = this.tags.map(item => item.metric_id);
    this.$emit('change', this.localValue);
  }

  /**
   * @description 选中
   * @param v
   */
  handleChecked(v: { checked: boolean; id: string }) {
    const fIndex = this.localValue.findIndex(id => v.id === id);
    if (v.checked) {
      fIndex < 0 && this.localValue.push(v.id);
    } else {
      fIndex >= 0 && this.localValue.splice(fIndex, 1);
    }
    this.$emit('change', this.localValue);
    this.handleGetMetricTag();
    this.$nextTick(() => {
      this.getOverflowHideCount();
    });
  }

  /**
   * @description 清空所有
   * @param e
   */
  handleClearAll(e: Event) {
    e.stopPropagation();
    this.localValue = [];
    this.handleGetMetricTag();
    this.$nextTick(() => {
      this.getOverflowHideCount();
    });
  }

  render() {
    return (
      <span
        class={['aiops-monitor-metric-select-component', { 'show-all': this.showAll }]}
        id={this.selectTargetId}
        onClick={this.handleClick}
      >
        <div class='tag-select-wrap'>
          {this.tags.map((item, index) => (
            <div
              key={item.metric_id}
              class='tag-item'
            >
              <span>{item.name}</span>
              <span
                class='icon-monitor icon-mc-close'
                onClick={e => this.handleDel(e, index)}
              ></span>
            </div>
          ))}
        </div>
        <div class='icon-monitor icon-arrow-down'></div>
        <div
          class='icon-monitor icon-mc-close-fill'
          onClick={e => this.handleClearAll(e)}
        ></div>
        <MetricSelector
          show={this.showSelector}
          targetId={`#${this.selectTargetId}`}
          type={MetricType.TimeSeries}
          scenarioList={this.scenarioList}
          customMetrics={this.metrics}
          multiple={true}
          metricIds={this.localValue}
          defaultScenario={this.defaultScenario}
          onShowChange={val => this.handleShowSelector(val)}
          onChecked={val => this.handleChecked(val)}
        ></MetricSelector>
      </span>
    );
  }
}
