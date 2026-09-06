# 实验 02 - Horizontal Pod Autoscaling（水平Pod自动扩缩）

## 目标

验证 Kubernetes 能否根据 CPU 使用率自动对应用进行扩缩容。

## 环境

- Kubernetes：K3s
- 节点数：3
- 应用：psre-api
- 初始副本数：3
- 最小副本数：3
- 最大副本数：6
- CPU 目标值：50%

## 初始状态

```text
副本数：3
CPU：低
```

## 生成负载

```bash
kubectl run hey \
  -n psre \
  --image=ricoli/hey \
  --restart=Never \
  -- \
  -z 5m \
  -c 100 \
  http://psre-api:8000/api/v1/work
```

`ricoli/hey` 是现成的 Docker 镜像，Docker Hub 上仍有该镜像；`hey` 本身支持 `-z` 和 `-c`。

![hpa_CPU资源对象](https://github.com/RS301/production-sre-platform/blob/main/images/hpa_CPU%E8%B5%84%E6%BA%90%E5%AF%B9%E8%B1%A1.png?raw=true)

测试完删除：

```bash
kubectl delete pod hey -n psre
```

## 预期行为

```
CPU 升高
    |
    v
HPA 检测到资源压力
    |
    v
3 个 Pod
    |
    v
4 个 Pod
    |
    v
5 个 Pod
    |
    v
6 个 Pod
```

![hpa_正在扩容](https://github.com/RS301/production-sre-platform/blob/main/images/hpa_%E6%AD%A3%E5%9C%A8%E6%89%A9%E5%AE%B9.png?raw=true)

恢复

负载停止后，HPA 会将应用缩容回最小副本数。

## 结果

![hpa_成功扩容](https://github.com/RS301/production-sre-platform/blob/main/images/hpa_%E6%88%90%E5%8A%9F%E6%89%A9%E5%AE%B9.png?raw=true)

自动扩缩容行为验证成功。
