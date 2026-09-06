实验 03：Kubernetes 可观测性建设
一、实验目的
本实验用于为 Production SRE Platform 建立第一套完整的可观测性体系。
实现以下监控链路：
Kubernetes Node
      |
      +----> Node Exporter
      |
      +----> kube-state-metrics
      |
      +----> Application Metrics
                    |
                    v
                Prometheus
                    |
                    v
                  Grafana
同时建立应用级核心指标：
●  请求量 
●  错误率 
●  P95 延迟 
●  Pod 重启次数 

二、实验环境
项目	配置
Kubernetes	K3s
Master	k8s-master
Worker 01	k8s-worker1
Worker 02	k8s-worker2
Application	psre-api
Monitoring	Prometheus
Dashboard	Grafana
Alerting	PrometheusRule

三、Prometheus 部署
使用 kube-prometheus-stack 部署监控体系。
主要组件：
●  Prometheus 
●  Grafana 
●  Alertmanager 
●  node-exporter 
●  kube-state-metrics 
●  Prometheus Operator 
检查：
kubectl get pods -n monitoring
预期：
所有核心监控组件均处于 Running 状态。

四、应用指标
PSRE API 提供：
/metrics
主要指标：
http_requests_total
http_request_duration_seconds
http_request_errors_total

五、ServiceMonitor
通过 ServiceMonitor 将：
psre-api
注册到 Prometheus。
配置：
Namespace: psre
Service: psre-api
Metrics Path: /metrics
Interval: 15s

六、Grafana
Grafana 用于展示：
●  Node CPU 
●  Node Memory 
●  Node Disk 
●  Kubernetes Pod 状态 
●  Pod Restart 
●  Request Rate 
●  Error Rate 
●  P95 Latency 

七、PrometheusRule
本实验建立以下告警：
PSREHighErrorRate
当错误率超过 5%，并持续 2 分钟：
severity: critical
PSREHighLatency
当 P95 延迟超过 300ms，并持续 5 分钟：
severity: warning
PSREPodRestarting
当 Pod 在 10 分钟内重启超过 3 次：
severity: warning

八、故障注入
使用以下命令持续制造 HTTP 500：
while true; do
  curl -s http://psre.local/api/v1/error > /dev/null
  sleep 0.2
done

九、实验过程
正常状态
    |
    v
错误率接近 0%
    |
    v
持续产生 HTTP 500
    |
    v
错误率持续上升
    |
    v
超过 5%
    |
    v
持续超过 2 分钟
    |
    v
Prometheus Rule 触发
    |
    v
PSREHighErrorRate = FIRING

十、实验结果
实验成功触发高错误率告警。
告警状态：
INACTIVE
    ->
PENDING
    ->
FIRING
停止故障注入后：
错误率下降
    |
    v
告警恢复
    |
    v
INACTIVE

十一、实验结论
本实验验证了以下完整链路：
应用故障
    |
    v
应用指标
    |
    v
Prometheus
    |
    v
PrometheusRule
    |
    v
告警
    |
    v
恢复
说明当前平台已经具备基础的应用可观测性和告警能力。实验 03：Kubernetes 可观测性建设
一、实验目的
本实验用于为 Production SRE Platform 建立第一套完整的可观测性体系。
实现以下监控链路：
Kubernetes Node
      |
      +----> Node Exporter
      |
      +----> kube-state-metrics
      |
      +----> Application Metrics
                    |
                    v
                Prometheus
                    |
                    v
                  Grafana
同时建立应用级核心指标：
●  请求量 
●  错误率 
●  P95 延迟 
●  Pod 重启次数 

二、实验环境
项目	配置
Kubernetes	K3s
Master	k8s-master
Worker 01	k8s-worker1
Worker 02	k8s-worker2
Application	psre-api
Monitoring	Prometheus
Dashboard	Grafana
Alerting	PrometheusRule

三、Prometheus 部署
使用 kube-prometheus-stack 部署监控体系。
主要组件：
●  Prometheus 
●  Grafana 
●  Alertmanager 
●  node-exporter 
●  kube-state-metrics 
●  Prometheus Operator 
检查：
kubectl get pods -n monitoring
预期：
所有核心监控组件均处于 Running 状态。

四、应用指标
PSRE API 提供：
/metrics
主要指标：
http_requests_total
http_request_duration_seconds
http_request_errors_total

五、ServiceMonitor
通过 ServiceMonitor 将：
psre-api
注册到 Prometheus。
配置：
Namespace: psre
Service: psre-api
Metrics Path: /metrics
Interval: 15s

六、Grafana
Grafana 用于展示：
●  Node CPU 
●  Node Memory 
●  Node Disk 
●  Kubernetes Pod 状态 
●  Pod Restart 
●  Request Rate 
●  Error Rate 
●  P95 Latency 

七、PrometheusRule
本实验建立以下告警：
PSREHighErrorRate
当错误率超过 5%，并持续 2 分钟：
severity: critical
PSREHighLatency
当 P95 延迟超过 300ms，并持续 5 分钟：
severity: warning
PSREPodRestarting
当 Pod 在 10 分钟内重启超过 3 次：
severity: warning

八、故障注入
使用以下命令持续制造 HTTP 500：
while true; do
  curl -s http://psre.local/api/v1/error > /dev/null
  sleep 0.2
done

九、实验过程
正常状态
    |
    v
错误率接近 0%
    |
    v
持续产生 HTTP 500
    |
    v
错误率持续上升
    |
    v
超过 5%
    |
    v
持续超过 2 分钟
    |
    v
Prometheus Rule 触发
    |
    v
PSREHighErrorRate = FIRING

十、实验结果
实验成功触发高错误率告警。
告警状态：
INACTIVE
    ->
PENDING
    ->
FIRING
停止故障注入后：
错误率下降
    |
    v
告警恢复
    |
    v
INACTIVE

十一、实验结论
本实验验证了以下完整链路：
应用故障
    |
    v
应用指标
    |
    v
Prometheus
    |
    v
PrometheusRule
    |
    v
告警
    |
    v
恢复
说明当前平台已经具备基础的应用可观测性和告警能力。实验 03：Kubernetes 可观测性建设
一、实验目的
本实验用于为 Production SRE Platform 建立第一套完整的可观测性体系。
实现以下监控链路：
Kubernetes Node
      |
      +----> Node Exporter
      |
      +----> kube-state-metrics
      |
      +----> Application Metrics
                    |
                    v
                Prometheus
                    |
                    v
                  Grafana
同时建立应用级核心指标：
●  请求量 
●  错误率 
●  P95 延迟 
●  Pod 重启次数 

二、实验环境
项目	配置
Kubernetes	K3s
Master	k8s-master
Worker 01	k8s-worker1
Worker 02	k8s-worker2
Application	psre-api
Monitoring	Prometheus
Dashboard	Grafana
Alerting	PrometheusRule

三、Prometheus 部署
使用 kube-prometheus-stack 部署监控体系。
主要组件：
●  Prometheus 
●  Grafana 
●  Alertmanager 
●  node-exporter 
●  kube-state-metrics 
●  Prometheus Operator 
检查：
kubectl get pods -n monitoring
预期：
所有核心监控组件均处于 Running 状态。

四、应用指标
PSRE API 提供：
/metrics
主要指标：
http_requests_total
http_request_duration_seconds
http_request_errors_total

五、ServiceMonitor
通过 ServiceMonitor 将：
psre-api
注册到 Prometheus。
配置：
Namespace: psre
Service: psre-api
Metrics Path: /metrics
Interval: 15s

六、Grafana
Grafana 用于展示：
●  Node CPU 
●  Node Memory 
●  Node Disk 
●  Kubernetes Pod 状态 
●  Pod Restart 
●  Request Rate 
●  Error Rate 
●  P95 Latency 

七、PrometheusRule
本实验建立以下告警：
PSREHighErrorRate
当错误率超过 5%，并持续 2 分钟：
severity: critical
PSREHighLatency
当 P95 延迟超过 300ms，并持续 5 分钟：
severity: warning
PSREPodRestarting
当 Pod 在 10 分钟内重启超过 3 次：
severity: warning

八、故障注入
使用以下命令持续制造 HTTP 500：
while true; do
  curl -s http://psre.local/api/v1/error > /dev/null
  sleep 0.2
done

九、实验过程
正常状态
    |
    v
错误率接近 0%
    |
    v
持续产生 HTTP 500
    |
    v
错误率持续上升
    |
    v
超过 5%
    |
    v
持续超过 2 分钟
    |
    v
Prometheus Rule 触发
    |
    v
PSREHighErrorRate = FIRING

十、实验结果
实验成功触发高错误率告警。
告警状态：
INACTIVE
    ->
PENDING
    ->
FIRING
停止故障注入后：
错误率下降
    |
    v
告警恢复
    |
    v
INACTIVE

十一、实验结论
本实验验证了以下完整链路：
应用故障
    |
    v
应用指标
    |
    v
Prometheus
    |
    v
PrometheusRule
    |
    v
告警
    |
    v
恢复
说明当前平台已经具备基础的应用可观测性和告警能力。实验 03：Kubernetes 可观测性建设
一、实验目的
本实验用于为 Production SRE Platform 建立第一套完整的可观测性体系。
实现以下监控链路：
Kubernetes Node
      |
      +----> Node Exporter
      |
      +----> kube-state-metrics
      |
      +----> Application Metrics
                    |
                    v
                Prometheus
                    |
                    v
                  Grafana
同时建立应用级核心指标：
●  请求量 
●  错误率 
●  P95 延迟 
●  Pod 重启次数 

二、实验环境
项目	配置
Kubernetes	K3s
Master	k8s-master
Worker 01	k8s-worker1
Worker 02	k8s-worker2
Application	psre-api
Monitoring	Prometheus
Dashboard	Grafana
Alerting	PrometheusRule

三、Prometheus 部署
使用 kube-prometheus-stack 部署监控体系。
主要组件：
●  Prometheus 
●  Grafana 
●  Alertmanager 
●  node-exporter 
●  kube-state-metrics 
●  Prometheus Operator 
检查：
kubectl get pods -n monitoring
预期：
所有核心监控组件均处于 Running 状态。

四、应用指标
PSRE API 提供：
/metrics
主要指标：
http_requests_total
http_request_duration_seconds
http_request_errors_total

五、ServiceMonitor
通过 ServiceMonitor 将：
psre-api
注册到 Prometheus。
配置：
Namespace: psre
Service: psre-api
Metrics Path: /metrics
Interval: 15s

六、Grafana
Grafana 用于展示：
●  Node CPU 
●  Node Memory 
●  Node Disk 
●  Kubernetes Pod 状态 
●  Pod Restart 
●  Request Rate 
●  Error Rate 
●  P95 Latency 

七、PrometheusRule
本实验建立以下告警：
PSREHighErrorRate
当错误率超过 5%，并持续 2 分钟：
severity: critical
PSREHighLatency
当 P95 延迟超过 300ms，并持续 5 分钟：
severity: warning
PSREPodRestarting
当 Pod 在 10 分钟内重启超过 3 次：
severity: warning

八、故障注入
使用以下命令持续制造 HTTP 500：
while true; do
  curl -s http://psre.local/api/v1/error > /dev/null
  sleep 0.2
done

九、实验过程
正常状态
    |
    v
错误率接近 0%
    |
    v
持续产生 HTTP 500
    |
    v
错误率持续上升
    |
    v
超过 5%
    |
    v
持续超过 2 分钟
    |
    v
Prometheus Rule 触发
    |
    v
PSREHighErrorRate = FIRING

十、实验结果
实验成功触发高错误率告警。
告警状态：
INACTIVE
    ->
PENDING
    ->
FIRING
停止故障注入后：
错误率下降
    |
    v
告警恢复
    |
    v
INACTIVE

十一、实验结论
本实验验证了以下完整链路：
应用故障
    |
    v
应用指标
    |
    v
Prometheus
    |
    v
PrometheusRule
    |
    v
告警
    |
    v
恢复
说明当前平台已经具备基础的应用可观测性和告警能力。实验 03：Kubernetes 可观测性建设
一、实验目的
本实验用于为 Production SRE Platform 建立第一套完整的可观测性体系。
实现以下监控链路：
Kubernetes Node
      |
      +----> Node Exporter
      |
      +----> kube-state-metrics
      |
      +----> Application Metrics
                    |
                    v
                Prometheus
                    |
                    v
                  Grafana
同时建立应用级核心指标：
●  请求量 
●  错误率 
●  P95 延迟 
●  Pod 重启次数 

二、实验环境
项目	配置
Kubernetes	K3s
Master	k8s-master
Worker 01	k8s-worker1
Worker 02	k8s-worker2
Application	psre-api
Monitoring	Prometheus
Dashboard	Grafana
Alerting	PrometheusRule

三、Prometheus 部署
使用 kube-prometheus-stack 部署监控体系。
主要组件：
●  Prometheus 
●  Grafana 
●  Alertmanager 
●  node-exporter 
●  kube-state-metrics 
●  Prometheus Operator 
检查：
kubectl get pods -n monitoring
预期：
所有核心监控组件均处于 Running 状态。

四、应用指标
PSRE API 提供：
/metrics
主要指标：
http_requests_total
http_request_duration_seconds
http_request_errors_total

五、ServiceMonitor
通过 ServiceMonitor 将：
psre-api
注册到 Prometheus。
配置：
Namespace: psre
Service: psre-api
Metrics Path: /metrics
Interval: 15s

六、Grafana
Grafana 用于展示：
●  Node CPU 
●  Node Memory 
●  Node Disk 
●  Kubernetes Pod 状态 
●  Pod Restart 
●  Request Rate 
●  Error Rate 
●  P95 Latency 

七、PrometheusRule
本实验建立以下告警：
PSREHighErrorRate
当错误率超过 5%，并持续 2 分钟：
severity: critical
PSREHighLatency
当 P95 延迟超过 300ms，并持续 5 分钟：
severity: warning
PSREPodRestarting
当 Pod 在 10 分钟内重启超过 3 次：
severity: warning

八、故障注入
使用以下命令持续制造 HTTP 500：
while true; do
  curl -s http://psre.local/api/v1/error > /dev/null
  sleep 0.2
done

九、实验过程
正常状态
    |
    v
错误率接近 0%
    |
    v
持续产生 HTTP 500
    |
    v
错误率持续上升
    |
    v
超过 5%
    |
    v
持续超过 2 分钟
    |
    v
Prometheus Rule 触发
    |
    v
PSREHighErrorRate = FIRING

十、实验结果
实验成功触发高错误率告警。
告警状态：
INACTIVE
    ->
PENDING
    ->
FIRING
停止故障注入后：
错误率下降
    |
    v
告警恢复
    |
    v
INACTIVE

十一、实验结论
本实验验证了以下完整链路：
应用故障
    |
    v
应用指标
    |
    v
Prometheus
    |
    v
PrometheusRule
    |
    v
告警
    |
    v
恢复
说明当前平台已经具备基础的应用可观测性和告警能力。
