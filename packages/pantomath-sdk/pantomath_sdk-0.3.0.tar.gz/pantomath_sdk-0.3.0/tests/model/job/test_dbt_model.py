from pantomath_sdk import DBTModelConstructor, PlatformTypes, Asset


def test_dbt_model_good():
    node = DBTModelConstructor(
        dbt_root_name="Root",
        account_id=146523457734567,
        package_name="package",
        job_name="DBTModelConstructor Unit Test",
        job_database_name="database",
        job_schema_name="schema",
    )
    assert node.get_name() == "DBTModelConstructor Unit Test Model"
    assert node.get_type() == "DBT_MODEL"
    assert (
        node.get_fully_qualified_object_name()
        == "root146523457734567.package.database.schema.dbtmodelconstructor unit test"
    )
    assert node.get_platform_type() == PlatformTypes.DBT.value
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "DBT", "type": "PLATFORM"}, {"depth": 1, "name": "Account Id - 146523457734567", "type": "CONNECTION"}]'
    )


def test_custom_dbt_model_asset_path_good():
    node = DBTModelConstructor(
        dbt_root_name="Root",
        account_id=146523457734567,
        package_name="package",
        job_name="DBTModelConstructor Unit Test",
        job_database_name="database",
        job_schema_name="schema",
        assets=[
            Asset("Factory", "FACTORY"),
        ],
    )
    assert (
        node.get_asset_path().__str__()
        == '[{"depth": 0, "name": "DBT", "type": "PLATFORM"}, {"depth": 1, "name": "Account Id - 146523457734567", "type": "CONNECTION"}, {"depth": 2, "name": "Factory", "type": "FACTORY"}]'
    )
