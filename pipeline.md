# 1. Models
## 1.1. Pipeline 
    -- Pipeline Name (should be a unique name)
    -- Pipeline Key ( created by the plaform, lower case, without spaces, without special characters, replace space with "_"). This will be a unique key.
    -- Project Name
    -- Created Data
    -- Created By
    -- Tags
    -- Git Branch
    -- Status (Active / Inactive)
## 1.2 Pipeline Definition
    -- Pipeline Id
    -- Pipeline JSON
    -- Created On
    -- Created By
    -- Update
## 1.3 Pipeline Validaton Error
    -- Transformation Name
    -- Error Message

# 2. End Points
## 2.1. Create Pipeline End Point
- Create Pipeline
- Create Pipeline Definition (placeholder entry in this tabele. Pipeline JSON will be empty)
- Pipeline Name and Pipleine Key should be unique

## 2.2. Autosave Pipeline Definition
- Input - Pipeline ID, (option - commmit / auto save) and JSON
- Process - From the JWT, get user details, update definition in the current row
- Mapping - Pipeline to pipeline definition is always one to one
- Validate the pipeline definition against schema and provide list of pipeline validation errors as output
- Challange - user will be option to redo incremental changes to the pipeline in the current session. To exploere how solutions like draw.io stores the user in progress work.

## 2.3. Commit Pipeline Definition
- Input - Pipeline ID, Commit message, minor/major version
- Process - From the JWT, get user details, take the latest json, uppdate/create branch, save the json into git respoisoty, add version number to the pipeline name

## 2.4. Get Pipeline Definition
- Input - Pipeline ID
- Response - Pipeline JSON

## 2.5. Disable Pipeline
- Input - Pipeline ID
- Process - Set "Status" to "Inactive" for the pipeline

## 2.6. Validate Pipeline
- Input - Pipeline ID
- Output - List of errors on the pipeline definition as per schemma "Pipeline Validaton Error"