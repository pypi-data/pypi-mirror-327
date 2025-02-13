
export CUDA_VISIBLE_DEVICES="0,3"
#export NCCL_DEBUG=INFO
export NCCL_SOCKET_IFNAME=bond0.100

torchrun \
    --nnodes=2 \
    --nproc-per-node=2 \
    --node-rank=1 \
    --rdzv-id=125 \
    --max-restarts=0 \
    --rdzv-endpoint="10.10.0.21:29999" \
    train.py \
    $@ \
    #--rdzv-backend=c10d \
