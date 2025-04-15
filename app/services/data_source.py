import json
from typing import Any, List, Optional
from app.core.config import Config
from app.models.data_source_layout import DataSourceLayout
from app.models.layout_fields import LayoutFields
from app.utils.data_source_utils import get_query_embedding, get_text_embedding
from sqlalchemy import select, join, and_, desc, or_, String, cast, func, text
from sqlalchemy.orm import joinedload
from app.models.bh_project import BHProject, LakeZone
import pgvector
from typing import Dict
from sqlalchemy.dialects.postgresql import ARRAY
import httpx
from app.models.data_source import (
    DataSource,
    DataSourceCreate,
    DataSourceUpdate,
    DataSourceReturn,
    DataSourceMetadata,
    DataSourceMetadataCreate,
    DataSourceMetadataUpdate,
    DataSourceMetadataReturn,
)
from app.services.base import BaseService
from app.core.context import Context
from fastapi import HTTPException
import numpy as np

class DataSourceService(BaseService):
    model: DataSource = DataSource
    create_model: DataSourceCreate = DataSourceCreate
    update_model: DataSourceUpdate = DataSourceUpdate
    return_schema: DataSourceReturn = DataSourceReturn
    name_field: str = 'data_src_name'
    key_field: str = 'data_src_key'

    def __init__(self, context: Context):
        super().__init__(context)

    async def search(self, params: Dict[str, str]) -> List[DataSourceReturn]:
        query = select(DataSource).filter(or_(DataSource.is_deleted == False, DataSource.is_deleted == None))

        vector_search_fields = ['data_src_name', 'data_src_desc']
        embedding_field = None
        for field, search_key in params.items():
            model_field = getattr(DataSource, field)

            if model_field.type == String:
                query = query.filter(or_(*[model_field.ilike(f'%{key}%') for key in search_key]))

            elif field in vector_search_fields:
                embedding = await get_text_embedding(search_key[0], "")

        if embedding:
            # Add the cosine similarity filtering and ordering to the query

            # embed_query = "SELECT data_src_embeddings <-> ${embedding}::vector AS distance FROM catalogdb.data_source LIMIT 10; "
            embedding_str = f'{embedding}'  # Ensure it's a properly formatted string for SQL

            # Use the embedding string in the query directly
            threshold = 0.8  # Set threshold for meaningful matches
            embed_query = f"""
                SELECT *, data_src_embeddings <-> '{embedding_str}'::vector AS distance
                FROM catalogdb.data_source
                WHERE data_src_embeddings <-> '{embedding_str}'::vector < '{threshold}'  -- Filter by distance threshold
                ORDER BY distance ASC
                LIMIT 10;
            """
        
            # results = await self.context.db_session.execute(text(embed_query), {"embedding": embedding_str})
            results = await self.context.db_session.execute(text(embed_query))

            # Retrieve all rows
            rows =  results.fetchall()


            data = [row for row in rows]

        # Return results as DataSourceReturn
        return data
        # return [DataSourceReturn.from_orm(result) for result in results.scalars()]

    

    async def check_source_exists(
            self,
            data_src_name: str = None,
            data_src_key: str = None,
        ):
        if data_src_name:
            data_src_key = self.name_to_key_parser(data_src_name)       
        statement = select(self.model).where(self.model.data_src_key == data_src_key)
        result = await self.context.db_session.execute(statement=statement)
        response = result.scalar_one_or_none()
        if response:
            return True
        return False

    async def get_all_datasets(
            self,
            bh_project_id: int = None,
            bh_project_cld_id: str = None,
            bh_project_name: str = None,
            lake_zone_id: int = None,
            lake_zone_cd: int = None,
            data_src_id: int = None,
            data_src_name: str = None,
            data_src_key: str = None,
        ):

        # Define the join condition
        join_condition = join(
            BHProject,
            LakeZone,
            BHProject.bh_project_id == LakeZone.bh_project_id
        ).join(
            DataSource,
            LakeZone.lake_zone_id == DataSource.lake_zone_id
        )

        # Start building the select statement
        statement = select(
            BHProject.bh_project_id,
            BHProject.bh_project_cld_id,
            BHProject.bh_project_name,
            LakeZone.lake_zone_id,
            LakeZone.lake_zone_cd,
            *DataSource.__table__.c  # Selects all fields from DataSource
        ).select_from(join_condition)

        # Initialize a list to hold filter conditions
        filters = []

        # Add filters based on provided parameters
        if bh_project_id:
            filters.append(BHProject.bh_project_id == bh_project_id)
        if bh_project_cld_id:
            filters.append(BHProject.bh_project_cld_id == bh_project_cld_id)
        if bh_project_name:
            filters.append(BHProject.bh_project_name == bh_project_name)
        if lake_zone_id:
            filters.append(LakeZone.lake_zone_id == lake_zone_id)
        if lake_zone_cd:
            filters.append(LakeZone.lake_zone_cd == lake_zone_cd)
        if data_src_id:
            filters.append(DataSource.data_src_id == data_src_id)
        if data_src_name:
            filters.append(DataSource.data_src_name == data_src_name)
        if data_src_key:
            filters.append(DataSource.data_src_key == data_src_key)

        # Apply filters to the statement if any filters were added
        if filters:
            statement = statement.where(and_(*filters))

        # Execute the query
        result = await self.context.db_session.execute(statement)
        response = result.all()

        return response
    
    async def get_all_datasets_by_project(
    self,
    bh_project_id: int = None,
    bh_project_cld_id: str = None,
    bh_project_name: str = None,
    lake_zone_id: int = None,
    lake_zone_cd: int = None,
    data_src_id: int = None,
    data_src_name: str = None,
    data_src_key: str = None,
    ):
    # Define the join condition
        join_condition = join(
            BHProject,
            LakeZone,
            BHProject.bh_project_id == LakeZone.bh_project_id
        ).join(
            DataSource,
            LakeZone.lake_zone_id == DataSource.lake_zone_id
        )

        # Start building the select statement
        statement = select(
            BHProject.bh_project_id,
            BHProject.bh_project_cld_id,
            BHProject.bh_project_name,
            LakeZone.lake_zone_id,
            LakeZone.lake_zone_cd,
            DataSource.data_src_id,
            DataSource.data_src_name,
            DataSource.data_src_desc,
            DataSource.created_at,
            DataSource.updated_at,
            DataSource.data_src_tags
        ).select_from(join_condition)

        # Initialize a list to hold filter conditions
        filters = []

        # Add filters based on provided parameters
        if bh_project_id:
            filters.append(BHProject.bh_project_id == bh_project_id)
        if bh_project_cld_id:
            filters.append(BHProject.bh_project_cld_id == bh_project_cld_id)
        if bh_project_name:
            filters.append(BHProject.bh_project_name == bh_project_name)
        if lake_zone_id:
            filters.append(LakeZone.lake_zone_id == lake_zone_id)
        if lake_zone_cd:
            filters.append(LakeZone.lake_zone_cd == lake_zone_cd)
        if data_src_id:
            filters.append(DataSource.data_src_id == data_src_id)
        if data_src_name:
            filters.append(DataSource.data_src_name == data_src_name)
        if data_src_key:
            filters.append(DataSource.data_src_key == data_src_key)

        # Apply filters to the statement if any filters were added
        if filters:
            statement = statement.where(and_(*filters))

        # Execute the query
        result = await self.context.db_session.execute(statement)
        rows = result.fetchall()

        # Process the results to group datasets by project and lake zone
        project_dict = {}
        for row in rows:
            project_id = row.bh_project_id
            if project_id not in project_dict:
                project_dict[project_id] = {
                    "bh_project_id": row.bh_project_id,
                    "bh_project_cld_id": row.bh_project_cld_id,
                    "bh_project_name": row.bh_project_name,
                    "lake_zone_id": row.lake_zone_id,
                    "lake_zone_cd": row.lake_zone_cd,
                    "data_set_list": [],
                    "created_at": row.created_at,
                    "updated_at": row.updated_at,
                    "data_src_tags": row.data_src_tags
                }
            project_dict[project_id]["data_set_list"].append({
                "data_src_id": row.data_src_id,
                "data_src_name": row.data_src_name,
                "data_src_desc": row.data_src_desc
            })

        return list(project_dict.values())
    
    async def list(
            self,
            offset: int = 0,
            limit: int = 10,
            order_by: Optional[str] = None,
            order_desc: bool = False,
            **kwargs,
            ) -> List[return_schema]:
        
        query = select(self.model).options(joinedload(self.model.bh_project)).where(or_(self.model.is_deleted == False, self.model.is_deleted == None))

        # To provide filter on input fields
        for kw in kwargs.keys():
            if kwargs.keys():
                if kwargs[kw] is not None:
                    query = query.where(getattr(self.model, kw) == kwargs[kw])

        query = query.offset(offset).limit(limit)
        
        if order_by:
            order_expression = getattr(self.model, order_by)
            if order_desc:
                order_expression = desc(order_expression)
            query = query.order_by(order_expression)

        results = await self.context.db_session.execute(query)

        return [
            self.return_schema(
                **vars(result),  
                bh_project_name=result.bh_project.bh_project_name if result.bh_project else None
            )
            for result in results.scalars()
        ]
    
    async def list_by_fields(
            self,
            offset: int = 0,
            limit: int = 10,
            order_by: Optional[str] = None,
            order_desc: bool = False,
            fields: Optional[str] = None,
            **kwargs,
        ) -> List[dict]:  # Return a list of dictionaries instead of schema objects

        query = select(self.model).options(joinedload(self.model.bh_project)).where(or_(self.model.is_deleted == False, self.model.is_deleted == None))

        # Apply filters based on input fields
        for kw in kwargs.keys():
            if kwargs.keys():
                if kwargs[kw] is not None:
                    query = query.where(getattr(self.model, kw) == kwargs[kw])

        query = query.offset(offset).limit(limit)

        # Apply ordering
        if order_by:
            order_expression = getattr(self.model, order_by)
            if order_desc:
                order_expression = desc(order_expression)
            query = query.order_by(order_expression)

        results = await self.context.db_session.execute(query)
        results = results.scalars().all()

        # Debug: Print what we are getting in `fields`
        print(f"Received fields: {fields}")

        # Convert `fields` from string to list, ensuring it's never None
        selected_fields = fields.split(",") if fields else []
        print(f"Parsed selected fields: {selected_fields}")

        # Ensure fields exist in the model
        model_columns = {column.name for column in self.model.__table__.columns}

        # Filter only valid fields
        valid_selected_fields = [field for field in selected_fields if field in model_columns]
        print(f"Valid selected fields: {valid_selected_fields}")

        response = []
        for result in results:
            if valid_selected_fields:
                formatted_data = {field: getattr(result, field, None) for field in valid_selected_fields}
            else:
                formatted_data = {column: getattr(result, column, None) for column in model_columns}

            # Include `bh_project_name` only if requested
            if "bh_project_name" in selected_fields or not selected_fields:
                formatted_data["bh_project_name"] = result.bh_project.bh_project_name if result.bh_project else None

            response.append(formatted_data)

        return response
    
    async def vector_search(self, params: Dict[str, str]) -> List[DataSourceReturn]:
        query = select(DataSource).filter(or_(DataSource.is_deleted == False, DataSource.is_deleted == None))

        parts = params.split(',')
    
        result_params = {
            "data_src_name": parts[0] if len(parts) > 0 else "",
            "data_src_desc": parts[1] if len(parts) > 1 else ""
        }

        embedding = await get_text_embedding(result_params["data_src_name"], result_params["data_src_desc"])

        if embedding:
            # Add the cosine similarity filtering and ordering to the query

            # embed_query = "SELECT data_src_embeddings <-> ${embedding}::vector AS distance FROM catalogdb.data_source LIMIT 10; "
            embedding_str = f'{embedding}'  # Ensure it's a properly formatted string for SQL

            # Use the embedding string in the query directly
            threshold = 0.8 
            embed_query = f"""
                SELECT *, data_src_embeddings <-> '{embedding_str}'::vector AS distance
                FROM catalogdb.data_source
                WHERE data_src_embeddings <-> '{embedding_str}'::vector < '{threshold}'  -- Filter by distance threshold
                ORDER BY distance ASC
                LIMIT 10;
            """
        
            results = await self.context.db_session.execute(text(embed_query))

            # Retrieve all rows
            rows =  results.fetchall()


            data = [row for row in rows]
        return data
    
    async def create_description(self, request: List[int]) -> dict:
        """
        Generate descriptions for multiple data sources and their columns using LLM.

        Args:
            request (List[int]): List of data source IDs.

        Returns:
            dict: Generated descriptions without updating embeddings.
        """
        try:
            cfg = Config()
            stmt = select(DataSource).where(DataSource.data_src_id.in_(request))
            data_sources = (await self.context.db_session.execute(stmt)).scalars().all()

            if not data_sources:
                raise HTTPException(status_code=404, detail="No matching data sources found")

            results = {}

            async with httpx.AsyncClient() as client:
                for ds in data_sources:
                    
                    stmt = select(LayoutFields).join(DataSourceLayout).where(DataSourceLayout.data_src_id == ds.data_src_id)
                    layout_fields = (await self.context.db_session.execute(stmt)).scalars().all()

                    ds_payload = {
                        "operation_type": "datasource_description",
                        "params": {
                            "schema": ", ".join(
                                [f"{lf.lyt_fld_name}: {lf.lyt_fld_data_type}" for lf in layout_fields]
                            ),
                            "target_column": ds.data_src_name
                        },
                        "thread_id": f"ds_{ds.data_src_id}"
                    }

                    response = await client.post(cfg.BH_AI_AGENT_URL, json=ds_payload)

                    if response.status_code != 200:
                        continue

                    ds_data = response.json()
                    ds_data = json.loads(ds_data.get("result", {}))

                    generated_description = ds_data.get("description")

                    if generated_description:
                        ds.data_src_desc = generated_description
                        results[ds.data_src_id] = {"data_source_description": generated_description}

                    column_payload = {
                        "operation_type": "column_description",
                        "params": {
                            "source_name": ds.data_src_name,
                            "columns": [
                                {"name": lf.lyt_fld_name, "data_type": lf.lyt_fld_data_type}
                                for lf in layout_fields
                            ]
                        },
                        "thread_id": f"columns_ds_{ds.data_src_id}"
                    }
                    column_response = await client.post(cfg.BH_AI_AGENT_URL, json=column_payload)

                    if column_response.status_code != 200:
                        continue

                    column_data = column_response.json()
                    column_data = json.loads(column_data.get("result", "{}"))
                    column_descriptions = column_data.get("descriptions", [])
                    for col_desc in column_descriptions:
                        for lf in layout_fields:
                            if lf.lyt_fld_name == col_desc.get("column_name"):
                                lf.lyt_fld_desc = col_desc.get("description")
                    
                    results[ds.data_src_id]["column_descriptions"] = column_descriptions
            await self.context.db_session.commit()
            return {"message": "Data source and column descriptions updated successfully", "results": results}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
          
    async def update_embeddings(self, request: List[int]) -> dict:
        try:
            
            stmt = select(DataSource).where(DataSource.data_src_id.in_(request))
            data_sources = (await self.context.db_session.execute(stmt)).scalars().all()

            if not data_sources:
                raise HTTPException(status_code=404, detail="No matching data sources found")

            results = {}
            for ds in data_sources:
                if not ds.data_src_desc:  
                    continue
                if not ds.data_src_relationships:
                    continue
                
                # get embedding for data source description
                ds_embedding = await get_text_embedding(ds.data_src_name, ds.data_src_desc, ds.data_src_relationships)
                ds.data_src_embeddings = ds_embedding[0] + ds_embedding[1]
                ds.data_src_relationships_embeddings = ds_embedding[2]
                # Fetch layout fields
                stmt = select(LayoutFields).join(DataSourceLayout).where(DataSourceLayout.data_src_id == ds.data_src_id)
                layout_fields = (await self.context.db_session.execute(stmt)).scalars().all()

                column_results = []

                for lf in layout_fields:
                    if not lf.lyt_fld_desc:  # Skip if no description exists
                        continue

                    # get embedding for column description
                    col_embedding = await get_text_embedding(lf.lyt_fld_name, lf.lyt_fld_desc)
                    lf.lyt_fld_embedding = col_embedding 

                    column_results.append({"column_name": lf.lyt_fld_name, "embedding_updated": True})

                results[ds.data_src_id] = {
                    "data_source_embedding_updated": True,
                    "column_embeddings_updated": column_results
                }

            await self.context.db_session.commit()
            return {"message": "Embeddings updated successfully", "results": results}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def semantic_search(self, user_query: str, connection_config_id: int) -> List[DataSourceReturn]:
        query_embedding, embedding = await get_query_embedding(user_query)

        embedding_str = f"'[{','.join(map(str, query_embedding))}]'"

       
        embed_query = f"""
            SELECT *, 
                1 - (data_src_embeddings <=> {embedding_str}::vector) AS similarity
            FROM catalogdb.data_source
            WHERE connection_config_id = :connection_config_id
            ORDER BY similarity DESC NULLS LAST
            LIMIT 50;  -- Increase the limit to 50 results
        """

        results = await self.context.db_session.execute(
            text(embed_query), {"connection_config_id": connection_config_id}
        )
        rows = results.fetchall()

        if not rows:
            return []

        similarities = np.array([row.similarity if row.similarity is not None else 0 for row in rows])

        # Lowering the threshold to include more results
        min_similarity_threshold = max(0.4, np.percentile(similarities,70))


        filtered_results = [
            row for row in rows if row.similarity is not None and row.similarity >= min_similarity_threshold
        ]

        return [DataSourceReturn.from_orm(row) for row in filtered_results]

    #TODO will remove after testing
    async def semantic_search2(self, user_query: str, connection_config_id: int) -> List[DataSourceReturn]:
        """
        Performs a two-step semantic search:
        1. Searches by data source name & description embeddings (1536-dim).
        2. Searches by relationship embeddings (768-dim).
        3. Merges and returns unique results.

        Args:
            user_query (str): The user's search query.
            connection_config_id (int): The ID of the connection configuration.

        Returns:
            List[DataSourceReturn]: A list of relevant data sources.
        """

        query_embedding, embedding = await get_query_embedding(user_query)

        embedding_str = f"'[{','.join(map(str, query_embedding))}]'"


        # Step 1: Search by data source description (1536-dim)
        desc_query = f"""
            SELECT *, 
                1 - (data_src_embeddings <=> {embedding_str}::vector) AS similarity
            FROM catalogdb.data_source
            WHERE connection_config_id = :connection_config_id
            ORDER BY similarity DESC NULLS LAST
            LIMIT 50;
        """

        # Step 2: Search by relationships (768-dim)
        relationship_embedding = embedding
        embedding_rel_str = f"'[{','.join(map(str, relationship_embedding))}]'"

        rel_query = f"""
            SELECT *, 
                1 - (data_src_relationships_embeddings <=> {embedding_rel_str}::vector) AS similarity
            FROM catalogdb.data_source
            WHERE connection_config_id = :connection_config_id
            ORDER BY similarity DESC NULLS LAST
            LIMIT 50;
        """

        # Execute both queries asynchronously
        results_desc = await self.context.db_session.execute(text(desc_query), {"connection_config_id": connection_config_id})
        results_rel = await self.context.db_session.execute(text(rel_query), {"connection_config_id": connection_config_id})

        desc_rows = results_desc.fetchall()
        rel_rows = results_rel.fetchall()

        if not desc_rows and not rel_rows:
            return []

        # Extract similarities
        desc_similarities = np.array([row.similarity if row.similarity is not None else 0 for row in desc_rows])
        rel_similarities = np.array([row.similarity if row.similarity is not None else 0 for row in rel_rows])

        # Apply similarity thresholds
        min_desc_similarity = max(0.4, np.percentile(desc_similarities, 70)) if len(desc_similarities) > 0 else 0.4
        min_rel_similarity = max(0.4, np.percentile(rel_similarities, 70)) if len(rel_similarities) > 0 else 0.4

        # Filter results
        filtered_desc_results = [row for row in desc_rows if row.similarity is not None and row.similarity >= min_desc_similarity]
        filtered_rel_results = [row for row in rel_rows if row.similarity is not None and row.similarity >= min_rel_similarity]

        # Merge results while ensuring uniqueness
        unique_results = {row[5]: row for row in filtered_desc_results}
        for row in filtered_rel_results:
            if row[5] not in unique_results:
                unique_results[row[5]] = row

        return [DataSourceReturn.from_orm(row) for row in unique_results.values()]



class DataSourceMetadataService(BaseService):
    model: DataSourceMetadata = DataSourceMetadata
    create_model: DataSourceMetadataCreate = DataSourceMetadataCreate
    update_model: DataSourceMetadataUpdate = DataSourceMetadataUpdate
    return_schema: DataSourceMetadataReturn = DataSourceMetadataReturn
    name_field: str = 'data_src_mtd_name'
    key_field: str = 'data_src_mtd_key'
