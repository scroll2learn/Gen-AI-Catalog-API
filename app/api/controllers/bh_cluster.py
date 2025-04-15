from app.utils.cloud_service_utils import get_cloud_decrypted_secrets
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.api.deps import get_context
from app.core.context import Context
from app.utils.auth_wrapper import authorize
from cluster.factory import ClusterFactory

from app.core.config import Config

router = APIRouter()

@router.post("/create-cluster", status_code=200)
async def create_cluster(
    cluster_name: str,
    bh_env_id: int,
    region: str = "us-east-1",
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
    ctx: Context = Depends(get_context)
):
    """
    API to create a new cluster.
    """
    if not authorized:
        raise HTTPException(status_code=403, detail="Unauthorized access.")

    cfg = Config()
    bh_env = await ctx.project_environment_service.get(id=bh_env_id)
    access_key, secret_access_key = await get_cloud_decrypted_secrets(bh_env.bh_env_name, cloud_type=cfg.CLOUD_TYPE, ctx=ctx)
    aws_cluster = ClusterFactory.get_cluster(
        cfg.CLOUD_TYPE,
        region=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key
    )

    try:
        response = aws_cluster.create_cluster(
            cluster_name=cluster_name,
            release_label="emr-6.7.0", 
            instance_type="m5.xlarge",
            instance_count=3
        )
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list-clusters", status_code=200)
async def list_clusters(
    bh_env_id: int,
    region: str = "us-east-1",
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
    ctx: Context = Depends(get_context)
):
    if not authorized:
        raise HTTPException(status_code=403, detail="Unauthorized access.")

    cfg = Config()
    bh_env = await ctx.project_environment_service.get(id=bh_env_id)
    access_key, secret_access_key = await get_cloud_decrypted_secrets(bh_env.bh_env_name, cloud_type=cfg.CLOUD_TYPE, ctx=ctx)
    
    aws_cluster = ClusterFactory.get_cluster(
        cfg.CLOUD_TYPE,
        region=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key
    )

    try:
        response = aws_cluster.list_clusters()
        return {"status": "success", "clusters": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cluster-status/{cluster_id}", status_code=200)
async def get_cluster_status(
    cluster_id: str,
    bh_env_id: int,
    region: str = "us-east-1",
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
    ctx: Context = Depends(get_context)
):
    if not authorized:
        raise HTTPException(status_code=403, detail="Unauthorized access.")

    cfg = Config()
    bh_env = await ctx.project_environment_service.get(id=bh_env_id)
    access_key, secret_access_key = await get_cloud_decrypted_secrets(bh_env.bh_env_name, cloud_type=cfg.CLOUD_TYPE, ctx=ctx)
    
    aws_cluster = ClusterFactory.get_cluster(
        cfg.CLOUD_TYPE,
        region=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key
    )

    try:
        response = aws_cluster.get_cluster_status(cluster_id)
        return {"status": "success", "cluster_status": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cluster-metrics/{cluster_id}", status_code=200)
async def get_cluster_metrics(
    cluster_id: str,
    bh_env_id: int,
    region: str = "us-east-1",
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
    ctx: Context = Depends(get_context)
):
    if not authorized:
        raise HTTPException(status_code=403, detail="Unauthorized access.")

    cfg = Config()
    bh_env = await ctx.project_environment_service.get(id=bh_env_id)
    access_key, secret_access_key = await get_cloud_decrypted_secrets(bh_env.bh_env_name, cloud_type=cfg.CLOUD_TYPE, ctx=ctx)
    
    aws_cluster = ClusterFactory.get_cluster(
        cfg.CLOUD_TYPE,
        region=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key
    )

    try:
        response = aws_cluster.get_cluster_metrics(cluster_id)
        return {"status": "success", "cluster_metrics": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cluster-configuration/{cluster_id}", status_code=200)
async def get_cluster_configuration(
    cluster_id: str,
    bh_env_id: int,
    region: str = "us-east-1",
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
    ctx: Context = Depends(get_context)
):
    if not authorized:
        raise HTTPException(status_code=403, detail="Unauthorized access.")

    cfg = Config()
    bh_env = await ctx.project_environment_service.get(id=bh_env_id)
    access_key, secret_access_key = await get_cloud_decrypted_secrets(bh_env.bh_env_name, cloud_type=cfg.CLOUD_TYPE, ctx=ctx)
    
    aws_cluster = ClusterFactory.get_cluster(
        cfg.CLOUD_TYPE,
        region=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key
    )

    try:
        response = aws_cluster.get_cluster_configuration(cluster_id)
        return {"status": "success", "cluster_configuration": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cluster-logs/{cluster_id}", status_code=200)
async def get_cluster_logs(
    cluster_id: str,
    bh_env_id: int,
    region: str = "us-east-1",
    authorized: Optional[dict] = Depends(authorize("admin_module", "view")),
    ctx: Context = Depends(get_context)
):
    if not authorized:
        raise HTTPException(status_code=403, detail="Unauthorized access.")

    cfg = Config()
    bh_env = await ctx.project_environment_service.get(id=bh_env_id)
    access_key, secret_access_key = await get_cloud_decrypted_secrets(bh_env.bh_env_name, cloud_type=cfg.CLOUD_TYPE, ctx=ctx)
    
    aws_cluster = ClusterFactory.get_cluster(
        cfg.CLOUD_TYPE,
        region=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key
    )

    try:
        response = aws_cluster.get_cluster_logs(cluster_id)
        return {"status": "success", "cluster_logs": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/terminate-cluster/{cluster_id}", status_code=200)
async def terminate_cluster(
    cluster_id: str,
    bh_env_id: int,
    region: str = "us-east-1",
    authorized: Optional[dict] = Depends(authorize("admin_module", "edit")),
    ctx: Context = Depends(get_context)
):
    if not authorized:
        raise HTTPException(status_code=403, detail="Unauthorized access.")

    cfg = Config()
    bh_env = await ctx.project_environment_service.get(id=bh_env_id)
    access_key, secret_access_key = await get_cloud_decrypted_secrets(bh_env.bh_env_name, cloud_type=cfg.CLOUD_TYPE, ctx=ctx)
    
    aws_cluster = ClusterFactory.get_cluster(
        cfg.CLOUD_TYPE,
        region=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key
    )

    try:
        success = aws_cluster.terminate_cluster(cluster_id)
        if success:
            return {"status": "success", "message": f"Cluster {cluster_id} termination requested."}
        else:
            raise HTTPException(status_code=500, detail="Failed to terminate cluster.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
