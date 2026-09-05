# Production SRE Platform

面向生产环境设计的 SRE 平台，用于 Kubernetes 集群运维、可观测性、自动化运维以及故障响应。

## 当前架构

```text
开发者
   |
   v
GitHub
   |
   v
容器镜像仓库（Container Registry）
   |
   v
K3s 集群
   |
   +------------------+
   |                  |
   v                  v
Worker01            Worker02
   |                  |
   +--------+---------+
            |
            v
         PSRE API
```

## 基础设施

| 节点          | CPU | 内存 | 角色                  | IP             |
| ----------- | --: | -: | ------------------- | -------------- |
| k8s-master  |  4C | 4G | 控制平面（Control Plane） | 192.168.17.128 |
| k8s-worker1 |  4C | 4G | 工作节点（Worker）        | 192.168.17.129 |
| k8s-worker2 |  4C | 4G | 工作节点（Worker）        | 192.168.17.130 |

## 技术栈

* Rocky Linux
* K3s
* Docker
* Kubernetes
* Python
* FastAPI
* Prometheus
* Grafana
* Terraform
* Ansible
* GitHub Actions

## 应用服务

项目包含一个基于 Python 和 FastAPI 构建的生产级 API 服务，目前提供：

* 健康检查（Health Check）
* 就绪检查（Readiness Check）
* Prometheus 指标接口
* 应用信息接口

## 项目路线图

### 基础设施

* [x] K3s 集群
* [x] Python API
* [x] Docker 镜像

### 容器化与 Kubernetes

* [ ] GitHub Container Registry（GHCR）
* [ ] Kubernetes Deployment
* [ ] Ingress
* [ ] HPA（Horizontal Pod Autoscaler）

### 可观测性

* [ ] Prometheus
* [ ] Grafana
* [ ] Alertmanager

### 自动化运维

* [ ] Terraform
* [ ] Ansible
* [ ] Python `opsctl`
* [ ] 自动化故障修复（Automated Remediation）

### 可靠性工程

* [ ] Chaos Engineering（混沌工程）
* [ ] Disaster Recovery（灾难恢复）
* [ ] GitHub Actions CI/CD

## 项目目标

Production SRE Platform 的目标是构建一个面向生产环境的 Kubernetes SRE 平台，将：

**基础设施 + 容器平台 + 可观测性 + 自动化运维 + 故障响应 + 可靠性工程**

整合到统一的平台中。

最终实现从代码提交、容器构建、部署发布，到监控、告警、故障定位以及自动化恢复的完整生产运维闭环。

