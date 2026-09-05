# 实验 01 - Kubernetes Pod 故障恢复

## 实验目标

验证 Kubernetes 在应用 Pod 发生故障后，是否能够自动重新创建 Pod，并恢复应用所需的副本数量。

## 实验环境

* Kubernetes：K3s
* Pod 副本数：3
* 应用：psre-api
* 节点：

  * k8s-master
  * k8s-worker1
  * k8s-worker2

## 初始状态

```text
3/3 Pods Running
```

表示当前共有 3 个 Pod，全部处于正常运行状态。

## 故障注入

手动删除一个 Pod，模拟应用 Pod 故障：

```bash
kubectl delete pod -n psre <pod-name>
```

例如：

```bash
kubectl delete pod -n psre psre-api-xxxxx
```

## 预期行为

```text
Pod 被删除
    |
    v
ReplicaSet 检测到副本数量不足
    |
    v
自动创建新的 Pod
    |
    v
Readiness Probe 检查通过
    |
    v
恢复为 3/3 Pods Running
```

## 实验结果

![故障自愈](https://github.com/RS301/production-sre-platform/blob/main/images/01.png?raw=true)

故障恢复成功。

Kubernetes 能够自动检测 Pod 副本数量不足，并创建新的 Pod 进行替换。

## 实验结论

Kubernetes 通过 Deployment 和 ReplicaSet 持续维持期望的副本数量。

当应用 Pod 被删除或发生故障时，Kubernetes 会自动创建新的 Pod，从而恢复应用服务的正常运行状态。

该实验验证了 Kubernetes 基础的 **Self-Healing（自愈）能力**。

