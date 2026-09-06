# Production SRE Platform

> 面向高级运维 / DevOps / SRE 岗位的云原生运维实验与自动化平台。

本项目基于 **K3s + Kubernetes + Docker + Python + Prometheus + Grafana + Traefik** 构建。

项目重点不是简单展示 Kubernetes YAML，而是通过实际的部署、监控、扩缩容、故障注入和告警实验，形成完整的：

```text
部署
  ↓
运行
  ↓
监控
  ↓
发现
  ↓
告警
  ↓
故障处理
  ↓
恢复
```

后续将继续扩展：

```text
Terraform
    ↓
Ansible
    ↓
GitHub Actions
    ↓
Python opsctl
    ↓
自动诊断
    ↓
自动修复
    ↓
Chaos Engineering
    ↓
Disaster Recovery
```

---

# 1. 项目定位

本项目用于展示实际生产环境中常见的高级运维能力：

* Linux 基础运维
* Docker 容器化
* K3s / Kubernetes 集群管理
* Kubernetes 应用部署
* Service / Ingress
* 健康检查
* 资源 requests / limits
* HPA 自动扩缩容
* Prometheus 指标采集
* Grafana 可视化
* PrometheusRule 告警
* 应用级监控
* 故障注入
* 故障恢复
* SRE 指标设计

最终目标：

> 建立一套从基础设施、应用部署、监控告警到故障诊断和自动修复的完整 SRE 实验平台。

---

# 2. 当前环境

## 2.1 HomeLab

当前使用 VMware NAT 搭建 K3s 三节点集群。

```text
                         HomeLab
                            │
                         VMware
                            │
                         NAT / VMnet8
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
      k8s-master         k8s-worker1      k8s-worker2
      4C / 4G            4C / 4G          4C / 4G
      192.168.17.128     192.168.17.129   192.168.17.130
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                         K3s Cluster
```

## 2.2 节点信息

| 节点          | CPU |  内存 |    磁盘 | IP             | 角色            |
| ----------- | --: | --: | ----: | -------------- | ------------- |
| k8s-master  |  4C | 4GB |  60GB | 192.168.17.128 | Control Plane |
| k8s-worker1 |  4C | 4GB | 约60GB | 192.168.17.129 | Worker        |
| k8s-worker2 |  4C | 4GB | 约60GB | 192.168.17.130 | Worker        |

> 当前环境为 HomeLab / 非生产环境，用于技术验证、实验和作品集展示。

---

# 3. 技术栈

## Infrastructure

* Rocky Linux 9.6
* VMware
* K3s
* Kubernetes

## Container

* Docker
* OCI Container Image
* GitHub Container Registry

## Application

* Python
* FastAPI
* pytest

## Networking

* Kubernetes Service
* Traefik
* Ingress
* VMware NAT

## Observability

* Prometheus
* Grafana
* Alertmanager
* node-exporter
* kube-state-metrics
* Prometheus Operator
* ServiceMonitor
* PrometheusRule

## Planned

* Terraform
* Ansible
* GitHub Actions
* GitLab CI
* Python opsctl
* Chaos Engineering
* Disaster Recovery

---

# 4. 项目架构

当前版本架构：

```text
                        Developer
                            │
                            │ git push
                            ▼
                         GitHub
                            │
                            ▼
                         GHCR
                            │
                            │ Docker Image
                            ▼
                    ┌─────────────────┐
                    │   K3s Cluster   │
                    └────────┬────────┘
                             │
                  ┌──────────┼──────────┐
                  │          │          │
                  ▼          ▼          ▼
             k8s-master   worker01    worker02
                             │
                             ▼
                         PSRE API
                             │
                  ┌──────────┼──────────┐
                  │          │          │
                  ▼          ▼          ▼
               Service     Ingress     HPA
                             │
                             ▼
                          Traefik
                             │
                             ▼
                            User


Observability:

PSRE API
    │
    │ /metrics
    ▼
ServiceMonitor
    │
    ▼
Prometheus
    │
    ├───────────────┐
    ▼               ▼
Grafana        PrometheusRule
                    │
                    ▼
                 Alert
```

---

# 5. 当前已经完成的功能

## Kubernetes

* [x] K3s 三节点集群
* [x] Namespace
* [x] Deployment
* [x] Service
* [x] ConfigMap
* [x] Traefik Ingress
* [x] Readiness Probe
* [x] Liveness Probe
* [x] Startup Probe
* [x] Resource Requests
* [x] Resource Limits
* [x] Rolling Update
* [x] HPA

## Application

* [x] FastAPI
* [x] `/`
* [x] `/health`
* [x] `/ready`
* [x] `/metrics`
* [x] `/api/v1/info`
* [x] `/api/v1/work`
* [x] `/api/v1/error`
* [x] Python Unit Test

## Container

* [x] Dockerfile
* [x] 非 root 用户运行容器
* [x] GHCR 镜像
* [x] 镜像版本管理

## Observability

* [x] Prometheus
* [x] Grafana
* [x] node-exporter
* [x] kube-state-metrics
* [x] ServiceMonitor
* [x] Application Metrics
* [x] Grafana Dashboard
* [x] PrometheusRule
* [x] 应用错误率监控

## Reliability Experiments

* [x] Pod Failure Recovery
* [x] HPA Autoscaling
* [x] Application Error Injection
* [x] Prometheus Alert
* [x] Alert Recovery

---

# 6. Application

PSRE API 是本项目的测试业务服务。

## API

### Root

```text
GET /
```

示例：

```json
{
  "application": "psre-api",
  "version": "0.2.1",
  "environment": "homelab",
  "status": "running"
}
```

### Health

```text
GET /health
```

用途：

> Kubernetes Liveness Probe

---

### Readiness

```text
GET /ready
```

用途：

> Kubernetes Readiness Probe

---

### Metrics

```text
GET /metrics
```

提供 Prometheus 指标：

```text
http_requests_total
http_request_duration_seconds
http_request_errors_total
```

---

### Error Injection

```text
GET /api/v1/error
```

该接口用于模拟 HTTP 500 应用故障。

示例：

```text
HTTP/1.1 500 Internal Server Error
```

用途：

> Prometheus 告警实验。

---

# 7. Docker

应用通过 Docker 进行容器化。

Docker 构建：

```bash
docker build \
  -t ghcr.io/你的GitHub用户名/psre-api:0.2.1 \
  -f docker/Dockerfile .
```

运行：

```bash
docker run --rm \
  -p 8000:8000 \
  ghcr.io/你的GitHub用户名/psre-api:0.2.1
```

验证：

```bash
curl http://127.0.0.1:8000/health
```

---

# 8. GitHub Container Registry

镜像使用 GHCR：

```text
ghcr.io/你的GitHub用户名/psre-api
```

版本采用显式 Tag：

```text
0.1.0
0.2.0
0.2.1
```

不使用：

```text
latest
```

镜像发布：

```bash
docker push \
  ghcr.io/你的GitHub用户名/psre-api:0.2.1
```

Kubernetes 从 GHCR 获取镜像。

---

# 9. Kubernetes Deployment

应用使用 3 副本：

```text
PSRE API

Pod 1 ── Worker01
Pod 2 ── Worker02
Pod 3 ── Worker01 / Worker02
```

查看：

```bash
kubectl get pods \
  -n psre \
  -o wide
```

查看 Deployment：

```bash
kubectl get deployment \
  -n psre
```

查看滚动发布：

```bash
kubectl rollout status \
  deployment/psre-api \
  -n psre
```

---

# 10. Ingress

K3s 使用 Traefik 作为 Ingress Controller。

当前应用：

```text
Browser
   │
   ▼
Traefik
   │
   ▼
Ingress
   │
   ▼
Service
   │
   ▼
PSRE API Pods
```

测试地址：

```text
http://psre.local
```

本地测试环境通过 hosts 文件解析：

```text
192.168.17.128 psre.local
```

---

# 11. HPA 自动扩缩容

PSRE API 配置：

```text
Minimum replicas: 3
Maximum replicas: 6
CPU target: 50%
```

查看：

```bash
kubectl get hpa \
  -n psre
```

查看详细信息：

```bash
kubectl describe hpa \
  psre-api \
  -n psre
```

预期：

```text
3 Pods
   │
   │ CPU Increase
   ▼
4 Pods
   │
   ▼
5 Pods
   │
   ▼
6 Pods
```

停止压力后，根据 HPA 缩容策略逐步回落。

---

# 12. Observability

本项目采用三层监控模型：

```text
Infrastructure
       │
       ▼
   Node Metrics
       │
       ▼
Kubernetes Metrics
       │
       ▼
Application Metrics
```

## Infrastructure Metrics

包括：

* CPU
* Memory
* Disk
* Network
* Load

由 node-exporter 等组件提供。

---

## Kubernetes Metrics

包括：

* Node 状态
* Pod 状态
* Pod Restart
* Deployment Replica
* Container CPU
* Container Memory

由 kube-state-metrics 等组件提供。

---

## Application Metrics

PSRE API 提供：

```text
http_requests_total
http_request_duration_seconds
http_request_errors_total
```

通过：

```text
ServiceMonitor
```

注册到 Prometheus。

---

# 13. Prometheus

Prometheus 使用：

```text
kube-prometheus-stack
```

部署。

主要组件：

```text
Prometheus
Grafana
Alertmanager
node-exporter
kube-state-metrics
Prometheus Operator
```

Prometheus 数据保留时间：

```text
3 days
```

> 当前配置面向 HomeLab 实验环境，不作为长期生产监控存储方案。

---

# 14. ServiceMonitor

应用监控流程：

```text
PSRE API
    │
    │ /metrics
    ▼
Service
    │
    ▼
ServiceMonitor
    │
    ▼
Prometheus
```

当前 ServiceMonitor：

```text
monitoring/prometheus/psre-api-servicemonitor.yaml
```

监控：

```text
Namespace: psre
Service: psre-api
Path: /metrics
Interval: 15s
```

---

# 15. Grafana

Grafana 用于展示：

```text
Node
Kubernetes
Application
```

当前已经验证：

* Node Dashboard
* Kubernetes Dashboard
* Prometheus Data Source
* PSRE API Metrics

---

## Grafana 访问

```text
http://grafana.psre.local
```

通过：

```text
Traefik
  ↓
Ingress
  ↓
Grafana Service
```

---

# 16. Prometheus

访问：

```text
http://prometheus.psre.local
```

主要用于：

* PromQL
* Target 检查
* Rule 检查
* Alert 检查

---

# 17. 常用 PromQL

## 查询应用错误指标

```promql
http_request_errors_total
```

## 查询错误请求速率

```promql
rate(http_request_errors_total[5m])
```

## 聚合错误请求速率

```promql
sum(rate(http_request_errors_total[5m]))
```

> 注意：`sum()` 默认会去掉 Label，因此结果可能显示为 `{}`。只要 `{}` 后面存在数值，这属于正常现象。

## 应用错误率

```promql
100 *
(
  sum(rate(http_request_errors_total[5m]))
  /
  sum(rate(http_requests_total[5m]))
)
```

## 按接口查看错误速率

```promql
sum by (path) (
  rate(http_request_errors_total[5m])
)
```

---

# 18. Prometheus 告警规则

当前包含：

```text
PSREHighErrorRate
PSREHighLatency
PSREPodRestarting
```

---

## PSREHighErrorRate

触发条件：

```text
Error Rate > 5%
```

持续：

```text
2 minutes
```

级别：

```text
critical
```

---

## PSREHighLatency

触发条件：

```text
P95 latency > 300ms
```

持续：

```text
5 minutes
```

级别：

```text
warning
```

---

## PSREPodRestarting

触发条件：

```text
Pod 10 分钟内重启次数 > 3
```

级别：

```text
warning
```

---

# 19. 一个重要的 Prometheus 排障案例

项目中实际遇到过：

```text
PrometheusRule 已经创建
        │
        ▼
Kubernetes 中存在
        │
        ▼
Prometheus Rules 页面看不到
```

排查 Prometheus：

```yaml
ruleSelector:
  matchLabels:
    release: kube-prometheus-stack
```

发现自定义 PrometheusRule 缺少：

```yaml
release: kube-prometheus-stack
```

修复后：

```text
PrometheusRule
      │
      ▼
release=kube-prometheus-stack
      │
      ▼
Prometheus
      │
      ▼
Rules
      │
      ▼
Alerts
```

这次问题也被记录在实验文档中。

---

# 20. 实验记录

所有重要实验均保存到：

```text
docs/labs/
```

当前实验：

```text
01-pod-failure.md
02-hpa-autoscaling.md
03-observability.md
```

---

# 21. 实验 01：Pod 故障恢复

目标：

> 验证 Kubernetes 在 Pod 故障之后是否能够自动恢复。

实验过程：

```text
3 Pods Running
      │
      ▼
删除一个 Pod
      │
      ▼
2 Pods Running
      │
      ▼
Deployment / ReplicaSet
发现副本不足
      │
      ▼
创建新 Pod
      │
      ▼
Readiness Probe
      │
      ▼
3 Pods Running
```

执行：

```bash
kubectl delete pod \
  -n psre \
  <pod-name>
```

观察：

```bash
kubectl get pods \
  -n psre \
  -o wide \
  -w
```

实验记录：

```text
docs/labs/01-pod-failure.md
```

---

# 22. 实验 02：HPA 自动扩容

目标：

> 验证应用 CPU 使用率升高后 Kubernetes 能够自动增加 Pod 数量。

实验过程：

```text
3 Pods
   │
   ▼
持续产生请求
   │
   ▼
CPU 上升
   │
   ▼
HPA
   │
   ▼
增加副本
   │
   ▼
4 → 5 → 6
```

实验记录：

```text
docs/labs/02-hpa-autoscaling.md
```

相关截图：

```text
images/hpa_CPU资源对象.png
images/hpa_正在扩容.png
images/hpa_成功扩容.png
```

---

# 23. 实验 03：可观测性

目标：

> 建立 Node、Kubernetes、Application 三层监控体系。

实验链路：

```text
Node
  │
  ▼
node-exporter
  │
  ▼
Prometheus
  │
  ▼
Grafana
```

Kubernetes：

```text
Kubernetes
     │
     ▼
kube-state-metrics
     │
     ▼
Prometheus
```

Application：

```text
PSRE API
   │
   ▼
/metrics
   │
   ▼
ServiceMonitor
   │
   ▼
Prometheus
```

实验记录：

```text
docs/labs/03-observability.md
```

---

# 24. 实验 04：应用错误告警

目标：

> 模拟真实应用故障，并验证 Prometheus 是否可以发现异常。

故障接口：

```text
/api/v1/error
```

返回：

```text
HTTP 500
```

故障链路：

```text
HTTP 500
    │
    ▼
http_request_errors_total
    │
    ▼
Prometheus
    │
    ▼
Error Rate > 5%
    │
    ▼
PSREHighErrorRate
    │
    ▼
PENDING
    │
    ▼
FIRING
    │
    ▼
停止故障
    │
    ▼
RESOLVED
```

相关截图：

```text
images/04-before-error.png
images/04-alert-firing.png
```

---

# 25. 截图目录

项目运行结果统一保存在：

```text
images/
```

---

# 26. 项目目录

```text
production-sre-platform/
│
├── README.md
│
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
│       └── test_main.py
│
├── docker/
│   └── Dockerfile
│
├── kubernetes/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── namespace.yaml
│   └── service.yaml
│
├── monitoring/
│   ├── alertmanager/
│   │
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── ingress.yaml
│   │
│   ├── helm/
│   │   └── kube-prometheus-stack-values.yaml
│   │
│   └── prometheus/
│       ├── ingress.yaml
│       ├── psre-api-servicemonitor.yaml
│       └── rules/
│           └── psre-api-rules.yaml
│
├── docs/
│   └── labs/
│       ├── 01-pod-failure.md
│       ├── 02-hpa-autoscaling.md
│       └── 03-observability.md
│
├── images/
│
├── terraform/
│
├── ansible/
│
├── opsctl/
│
└── .github/
    └── workflows/
```

---

# 27. 快速开始

## 查看集群

```bash
kubectl get nodes -o wide
```

## 查看所有系统 Pod

```bash
kubectl get pods -A -o wide
```

## 查看业务

```bash
kubectl get all -n psre
```

## 查看监控

```bash
kubectl get pods -n monitoring
```

## 查看 Ingress

```bash
kubectl get ingress -A
```

---

# 28. 部署应用

```bash
kubectl apply \
  -f kubernetes/
```

检查：

```bash
kubectl get pods \
  -n psre \
  -o wide
```

检查：

```bash
kubectl get svc \
  -n psre
```

检查：

```bash
kubectl get ingress \
  -n psre
```

---

# 29. 部署监控

创建监控 Namespace：

```bash
kubectl create namespace monitoring
```

安装：

```text
kube-prometheus-stack
```

使用配置：

```text
monitoring/helm/kube-prometheus-stack-values.yaml
```

然后部署：

```bash
kubectl apply \
  -f monitoring/prometheus/psre-api-servicemonitor.yaml
```

Prometheus Rule：

```bash
kubectl apply \
  -f monitoring/prometheus/rules/psre-api-rules.yaml
```

---

# 30. 项目开发原则

本项目遵循以下原则：

### 1. 代码优先

所有重要操作尽可能转化为：

```text
Git
+
YAML
+
Python
+
Terraform
+
Ansible
```

而不是长期依赖手工操作。

### 2. 可重复

环境应尽量能够通过代码重复部署。

### 3. 可观测

所有重要应用都应该尽可能提供：

```text
Metrics
Health
Readiness
Logs
```

### 4. 可恢复

对故障不只是监控，还需要：

```text
Detect
Diagnose
Remediate
Verify
```

### 5. 可审计

每一次重要变更都进入：

```text
Git Commit
```

---

# 31. Roadmap

## V1.0

当前阶段：

```text
[x] K3s Cluster
[x] Python API
[x] Docker
[x] GHCR
[x] Kubernetes Deployment
[x] Service
[x] Traefik Ingress
[x] HPA
[x] Prometheus
[x] Grafana
[x] ServiceMonitor
[x] PrometheusRule
[x] Application Alert
```

## V1.1

下一阶段：

```text
[ ] Alertmanager Notification
[ ] SLO
[ ] SLI
[ ] Error Budget
[ ] Node Failure Alert
[ ] Pod CrashLoop Alert
[ ] Disk Pressure Alert
```

## V1.2

Infrastructure Automation：

```text
[ ] Terraform
[ ] Ansible
[ ] Linux Baseline
[ ] Kubernetes Bootstrap
```

## V1.3

CI/CD：

```text
[ ] GitHub Actions
[ ] GitLab CI
[ ] Automated Test
[ ] Docker Build
[ ] Image Security Scan
[ ] Automated Deployment
[ ] Automated Rollback
```

## V1.4

SRE Automation：

```text
[ ] Python opsctl
[ ] Cluster Health
[ ] Diagnosis
[ ] Incident
[ ] Remediation
```

## V2.0

Reliability Engineering：

```text
[ ] Chaos Engineering
[ ] Disaster Recovery
[ ] Backup / Restore
[ ] MTTR
[ ] SLO Dashboard
[ ] Automated Self-Healing
```

---

# 32. 最终目标

最终平台将形成：

```text
                       Developer
                           │
                           ▼
                         GitHub
                           │
                           ▼
                    GitHub Actions
                           │
                   Test / Build / Scan
                           │
                           ▼
                          GHCR
                           │
                           ▼
                     Kubernetes
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
           Application   Monitoring   Automation
              │            │            │
              │            ▼            │
              │        Prometheus       │
              │            │            │
              │            ▼            │
              │         Grafana         │
              │            │            │
              │            ▼            │
              │       Alertmanager      │
              │            │            │
              └────────────┼────────────┘
                           ▼
                       Python opsctl
                           │
                    ┌──────┼──────┐
                    ▼      ▼      ▼
                 Diagnose Remediate Rollback
                    │      │      │
                    └──────┼──────┘
                           ▼
                        Verify
                           │
                           ▼
                         SRE
```

---

# 33. 项目核心能力

本项目最终希望证明以下能力：

```text
Linux
  ↓
Container
  ↓
Kubernetes
  ↓
Infrastructure as Code
  ↓
Configuration Management
  ↓
CI/CD
  ↓
Observability
  ↓
Incident Response
  ↓
Automation
  ↓
Self-Healing
  ↓
SRE
```

> 本项目所有实验均基于 HomeLab 环境完成，实验中的性能、可用性和恢复时间数据均属于实验数据，不代表真实生产环境指标。

