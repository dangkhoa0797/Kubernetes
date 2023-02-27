#!/bin/bash
kubectl get configmap kube-proxy -n kube-system -o yaml > kubeproxy.yaml && sed -i "s/strictARP:.*$/strictARP: true/g" kubeproxy.yaml && kubectl replace -f kubeproxy.yaml