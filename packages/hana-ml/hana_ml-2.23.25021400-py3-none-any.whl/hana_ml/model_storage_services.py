#pylint: disable=too-many-lines
"""
This module implements the base class to enable saving and loading in the ML model classes.
"""
import json
import logging

from hdbcli import dbapi
import hana_ml#pylint:disable=unused-import
from hana_ml.ml_base import execute_logged, quotename
from hana_ml.model_storage import ModelStorageError
from hana_ml.dataframe import data_manipulation
from hana_ml.dataframe import DataFrame

logger = logging.getLogger(__name__) #pylint: disable=invalid-name

# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=no-else-return
# pylint: disable=bare-except
# pylint: disable=attribute-defined-outside-init
# pylint: disable=line-too-long
# pylint: disable=too-many-arguments
# pylint: disable=consider-using-f-string
# pylint: disable=broad-except
class ModelSavingServices(object): #pylint: disable=useless-object-inheritance
    """
    The base class to enable saving and loading in the ML model classes.
    It provides the following services to the ModelStorage class:
        - Encoding or Decoding the JSON string,
        - Saving the back-end model into table.

    The JSON string must have the following structure:
    It contains two blocks:
            - model_attributes: information to be saved/restored from/to the model object in python
            - artifacts: information about the model table
    For example:
        {
            "model_attributes": {
                "log_level": 8,
                "model_format": "bin",
                "language": "en",
                "variable_auto_selection": false,
                "name": "My Model 001",
                "version": 1
            },
            "artifacts": {
                "schema": "USER_APL",
                "model_tables": {"model_": "HANAML_APL_MODELS_DEFAULT"}
            }
        }
    """
    def __init__(self):
        self.name = None
        self.version = 1

    # ===== Methods callable from model_storage

    def is_fitted(self):
        r"""
        Checks if the model can be saved.
        To be overridden if the model is not stored in model\_ attribute.

        Returns
        -------
        bool
            True if the model is ready to be saved.
        """
        if hasattr(self, 'model_'):
            return getattr(self, 'model_') is not None
        return False

    def _encode_and_save(self, schema, storage_type, force=False, data_lake_container='SYSRDL#CG'):
        """
        Encodes the model as a JSON string and saves the model into a permanent table.
        This method is called from a ModelStorage instance to save the current model.

        Returns
        -------
        json: str
            The json string to be saved with metadata by ModelStorage.
        """
        # Encodes to JSON string
        js_str, model_table_names = self._encode(schema)
        # Saves the model table(s) into the model_table
        self._save_model_tables(schema=schema,
                                model_table_names=model_table_names,
                                storage_type=storage_type,
                                force=force,
                                data_lake_container=data_lake_container)
        return js_str

    @classmethod
    def _load_model(cls, connection_context, name, version, js_str):
        # pylint: disable=too-many-function-args, syntax-error
        """
        Loads a model.
        This method is called from a ModelStorage instance to reinstantiate a saved model.

        Parameters
        ----------
        model_cls: a model class
            The current model class
        connection_context: ConnectionContext
            The holder of SAP HANA connection. No need for PAL functions.
        name: str
            The model name
        version: int
            The model version
        js_str: str
            The model JSON string. It contains information about the model storage.

        Returns
        -------
        PAL/APL object
            A new instance of hana_ml model.
        """

        # Create a new model instance
        js_dict = json.loads(js_str)
        hanaml_parameters = js_dict['model_attributes']
        model = None
        try:
            if 'func' in hanaml_parameters:#for unified interface functions
                func = hanaml_parameters['func']
                model = cls(func, **hanaml_parameters['kwargs'])
            elif 'steps' in hanaml_parameters:#for Pipeline, need to evaluate the Pipeline string firstly
                steps = hanaml_parameters['steps']
                other_params = hanaml_parameters.copy()#make a copy for safty reason
                del other_params['steps']
                exec(f'e_steps = {steps}')#pylint:disable=exec-used
                model = cls(eval('e_steps'), **other_params)#pylint:disable=eval-used
            else:
                model = cls(**hanaml_parameters)
        except:
            model = cls()
        # Decodes the json and creates the model temporary table
        # pylint: disable=protected-access
        model._decode(name=name, version=version, js_str=js_str, conn_context=connection_context)
        # pal_meta for function, for APL it should be {}.
        if 'pal_meta' in js_dict:
            for at_name, at_val in js_dict['pal_meta'].items():
                setattr(model, at_name, at_val)
        if 'fit_params' in js_dict:
            setattr(model, 'hanaml_fit_params', js_dict['fit_params'])
        if 'model_card' in js_dict:
            setattr(model, 'model_card_', js_dict['model_card'])
        model.name = name
        model.version = version
        return model

    @staticmethod
    def _enable_persistent_memory(connection_context, name, version, js_str): #pylint: disable=unused-argument
        """
        Enable persistent memory.

        Parameters
        ----------
        connection_context: ConnectionContext
            The holder of SAP HANA connection
        name: str
            The model name
        version: str
            The model version
        js_str: str
            The model JSON string. It contains information about the model table.
        """
        js_dict = json.loads(js_str)
        schema = js_dict['artifacts']['schema']
        model_table_names = js_dict['artifacts']['model_tables']
        if isinstance(model_table_names, str):
            model_table_names = [model_table_names]
        for table_name in model_table_names:
            cur = connection_context.connection.cursor()
            sql = "ALTER TABLE {}.{} PERSISTENT MEMORY ON IMMEDIATE CASCADE"\
                .format(quotename(schema), quotename(table_name))
            cur.execute(sql)
            cur.close()
            connection_context.connection.commit()

    @staticmethod
    def _disable_persistent_memory(connection_context, name, version, js_str): #pylint: disable=unused-argument
        """
        Disable persistent memory.

        Parameters
        ----------
        connection_context: ConnectionContext
            The holder of SAP HANA connection
        name: str
            The model name
        version: str
            The model version
        js_str: str
            The model JSON string. It contains information about the model table.
        """

        js_dict = json.loads(js_str)
        schema = js_dict['artifacts']['schema']
        model_table_names = js_dict['artifacts']['model_tables']
        if isinstance(model_table_names, str):
            model_table_names = [model_table_names]
        for table_name in model_table_names:
            cur = connection_context.connection.cursor()
            sql = "ALTER TABLE {}.{} PERSISTENT MEMORY OFF IMMEDIATE CASCADE"\
                .format(quotename(schema), quotename(table_name))
            cur.execute(sql)
            cur.close()
            connection_context.connection.commit()

    @staticmethod
    def _load_mem(connection_context, name, version, js_str, **kwargs): #pylint: disable=unused-argument
        """
        Load model to memory.

        Parameters
        ----------
        connection_context: ConnectionContext
            The holder of SAP HANA connection
        name: str
            The model name
        version: str
            The model version
        js_str: str
            The model JSON string. It contains information about the model table.
        """
        js_dict = json.loads(js_str)
        schema = js_dict['artifacts']['schema']
        model_table_names = js_dict['artifacts']['model_tables']
        if isinstance(model_table_names, str):
            model_table_names = [model_table_names]
        for table_name in model_table_names:
            data_manipulation(connection_context, table_name, unload=False, schema=schema, **kwargs)

    @staticmethod
    def _unload_mem(connection_context, name, version, js_str, **kwargs): #pylint: disable=unused-argument
        """
        Unload model from memory.

        Parameters
        ----------
        connection_context: ConnectionContext
            The holder of SAP HANA connection
        name: str
            The model name
        version: str
            The model version
        js_str: str
            The model JSON string. It contains information about the model table.
        """
        js_dict = json.loads(js_str)
        schema = js_dict['artifacts']['schema']
        model_table_names = js_dict['artifacts']['model_tables']
        if isinstance(model_table_names, str):
            model_table_names = [model_table_names]
        for table_name in model_table_names:
            data_manipulation(connection_context, table_name, unload=True, schema=schema, **kwargs)

    @staticmethod
    def _delete_model(connection_context, name, version, js_str, storage_type, data_lake_container='SYSRDL#CG'):
        """
        Deletes the current model.
        This method is called from a ModelStorage instance to delete a saved model.

        Parameters
        ----------
        connection_context: ConnectionContext
            The holder of SAP HANA connection
        name: str
            The model name
        version: str
            The model version
        js_str: str
            The model JSON string. It contains information about the model table.
        storage_type : str, optional
            Specifies the storage type of the model:
                - 'default' : HANA default storage.
                - 'HDL' : HANA data lake.
        """
        # Gets the model schema and table name from js_str
        js_dict = json.loads(js_str)
        schema = js_dict['artifacts']['schema']
        model_table_names = js_dict['artifacts']['model_tables']
        lib = js_dict['artifacts']['library']
        # Deletes rows in model tables (APL) / Drop tables (PAL)
        if isinstance(model_table_names, str):
            model_table_names = [model_table_names]
        for table_name in model_table_names:
            with connection_context.connection.cursor() as cursor:
                if lib == 'APL':
                    if storage_type == 'HDL':
                        connection_context.drop_table(table=table_name,
                                                      data_lake=True,
                                                      data_lake_container=data_lake_container)
                    sql = 'delete from {schema_name}.{table_name}'.format(
                        schema_name=quotename(schema),
                        table_name=quotename(table_name))
                    sql = sql + " where NAME=? and VERSION=?"
                    param_vals = [name, int(version)]
                    logger.info("Executing SQL: %s %s", sql, param_vals)
                    cursor.execute(sql, param_vals)
                else:
                    # Drop virtual table/table
                    connection_context.drop_table(table=table_name, schema=schema)
                    # Drop the data lake table if exists
                    if storage_type == 'HDL':
                        data_lake_table_name = table_name
                        connection_context.drop_table(table=data_lake_table_name,
                                                      data_lake=True,
                                                      data_lake_container=data_lake_container)
                    connection_context.connection.commit()

    def _encode(self, schema):
        """
        Encodes a model as JSON string.
        This method can be overridden by specialized model classes.
        The returned JSON string must contains two blocks of information:
        - "model_attributes":
            It contains the information necessary to restore the python model object.
        - "artifacts":
            It contains the information about the model table.

        Returns
        -------
        str
            The JSON string.

        str
            The model table name
        """
        model = self
        # Prepares a dictionary that holds all data to be serialized as JSON
        js_dict = {}
        # Model parameters
        model_params = {}
        fit_params = {}
        # Gets all attributes that are of type (int, str, float) and name not started/ended with '_'
        for att_name in model.__dict__:
            # Excludes the attributes that are not to be saved
            p_count = 0
            if att_name in ['id']:
                continue
            if att_name.startswith('_'):
                continue
            if att_name.endswith('_'):
                continue
            att_val = getattr(model, att_name)
            att_type = type(att_val)
            if self._is_APL():
                if att_type in [int, float, str, bool] or \
                   att_name in ['other_train_apl_aliases']:
                    model_params[att_name] = att_val
            else:
                try:
                    if 'hanaml_parameters' in att_name:
                        model_params = att_val
                        p_count = p_count + 1
                    if 'hanaml_fit_params' in att_name:
                        fit_params = att_val
                        p_count = p_count + 1
                    if p_count >= 2:
                        break
                except Exception as err:
                    logger.warning(err)
                    pass
        js_dict['model_attributes'] = model_params
        js_dict['fit_params'] = fit_params
        # Artifacts
        artifacts = {}
        artifacts['schema'] = schema
        # pylint: disable=protected-access
        model_tables = model._get_model_table_names()  # dict {'model attribute': 'table_name'}
        artifacts['model_tables'] = model_tables
        artifacts['library'] = 'PAL'
        if self._is_APL():
            artifacts['library'] = 'APL'
        js_dict['artifacts'] = artifacts

        pal_meta = {}
        if not self._is_APL():
            if model._fit_anonymous_block:
                pal_meta["_fit_anonymous_block"] = model._fit_anonymous_block
            if model._fit_param:
                pal_meta["_fit_param"] = model._fit_param
            if model._predict_param:
                pal_meta["_predict_param"] = model._predict_param
            if hasattr(model, 'fit_data'):
                if isinstance(model.fit_data, DataFrame):
                    pal_meta["fit_data_struct"] = model.fit_data.get_table_structure()
            if hasattr(model, 'predict_data'):
                if isinstance(model.predict_data, DataFrame):
                    pal_meta["predict_data_struct"] = model.predict_data.get_table_structure()
            if hasattr(model, 'label'):
                pal_meta["label"] = model.label
            if hasattr(model, 'runtime'):
                pal_meta["runtime"] = model.runtime
        js_dict['pal_meta'] = pal_meta
        if hasattr(model, 'model_card_'):
            js_dict['model_card'] = model.model_card_
        # Gets the final json to be saved
        js_str = json.dumps(js_dict)
        return js_str, model_tables

    def _decode(self, name, version, js_str, conn_context=None):
        """
        Decodes the JSON string:
        - Reinstantiates the model,
        - Loads the model content into temporary table,
        - Restores the model attributes.

        Parameters
        ----------
        str
            The model name

        int
            The model version

        str
            The json string

        """
        js_dict = json.loads(js_str)
        if self._is_APL():
            for at_name, at_val in js_dict['model_attributes'].items():
                setattr(self, at_name, at_val)
        # Creates artifact on the back-end model
        schema = js_dict['artifacts']['schema']
        model_tables = js_dict['artifacts']['model_tables']
        self._load_model_tables(schema_name=schema,
                                model_table_names=model_tables,
                                name=name,
                                version=version,
                                conn_context=conn_context)

    def _is_APL(self):
        model = self
        if model.__module__.startswith('hana_ml.algorithms.apl'):
            return True
        return False

    def _get_model_table_names(self):
        """
        Returns a list of table name(s) where the end model is saved.
        This method has to be overridden if there are multiple tables to be returned.

        Returns
        -------
        list
            model_table_names
        """
        if self._is_APL():
            # return {'model_': 'HANAML_{}_MODELS_DEFAULT'.format('APL')}
            return ['HANAML_{}_MODELS_DEFAULT'.format('APL')]
        model_names = 'HANAML_{}_{}_MODELS'.format(self.name.replace(' ', '_').upper(), \
        self.version)
        if not isinstance(self.model_, list):
            return model_names
        model_names_lst = []
        for i in range(len(self.model_)):
            model_names_lst.append(model_names + '_'  + str(i))
        return model_names_lst

    def _check_table_exists(self, schema, table_name):
        """
        Checks if the <schema>.<table_name> exists.

        Parameters
        ----------
        schema: str
            The schema name
        table_name; str
            The table name

        Returns
        -------
        bool
            True if the table exists.
        """
        conn_context = getattr(self, 'conn_context')
        with conn_context.connection.cursor() as cursor:
            try:
                sql = 'select 1 from {schema_name}.{table_name} limit 1'.format(
                    schema_name=quotename(schema),
                    table_name=quotename(table_name))
                execute_logged(cursor, sql, conn_context.sql_tracer, conn_context)
                return True
            except dbapi.Error as err:
                if err.errorcode == 259:  # Invalid table name (unexisting table)
                    return False
                elif err.errorcode == 258:  # Insufficient privilege: Not authorized
                    raise ModelStorageError('The current user cannot read the metadata table. '
                                            + err.errortext)
                raise ModelStorageError('Database issue: ' + err.errortext)
            except Exception as err:
                if "(259)" in str(err):
                    return False
                elif "(258)" in str(err):  # Insufficient privilege: Not authorized
                    raise ModelStorageError('The current user cannot read the metadata table. '
                                            + str(err))
                raise ModelStorageError('Database issue: ' + str(err))

    def _save_model_tables(self, schema, model_table_names, storage_type, force=False, data_lake_container='SYSRDL#CG'):
        """
        Saves the model into the permanent table.

        Parameters
        ----------
        schema: str
            The schema name
        model_table_names: dict
            The dictionary maps the model attribute (for example, 'model_') to the model table name.
        storage_type : str, optional
            Specifies the storage type of the model:
                - 'default' : HANA default storage.
                - 'HDL' : HANA data lake.
        force : bool, optional
            Drop the existing table if True.
        """
        if self._is_APL():
            # Dataframe: temp table containing the original APL model as returned by APL API
            artifact_df = getattr(self, 'model_', None)
            # The table name (HANAML_APL_MODELS_DEFAULT) where to store permanently the new model
            table_name = model_table_names[0]

            # Select the original model table Columns to be saved
            # col_names = 'NAME, VERSION, col1, col2, ..., coln'
            col_names = "cast('{name}' as varchar(255)) NAME, {version} VERSION, ".format(
                name=self.name.replace("'", "''"),
                version=self.version
            )
            # col_names = col_names + functools.reduce(
            #     (lambda x, y: x + ',' + y),
            #     [quotename(colname) for colname in artifact_df.columns])
            col_names = col_names + ','.join([quotename(colname)
                                              for colname in artifact_df.columns])
            # FPA78-4342: support HDL
            select_stmt = "select {col_names} from {source_schema}.{source_table}".format(
                col_names=col_names,
                source_schema=artifact_df.source_table['SCHEMA_NAME'],
                source_table=artifact_df.source_table['TABLE_NAME'],
            )
            # Saves the model content into HANAML_APL_MODELS_DEFAULT via DataFrame
            model_df = DataFrame(self.conn_context, select_stmt)
            if storage_type == 'HDL':
                model_df.save(where=table_name,
                              data_lake=True,
                              force=force,
                              append=True,
                              data_lake_container=data_lake_container)
            else:
                model_df.save(where=(schema, table_name),
                              data_lake=False,
                              force=force,
                              append=True,
                              data_lake_container=data_lake_container)
        else:
            if not isinstance(self.model_, (list, tuple)):
                if storage_type == 'HDL':
                    self.model_.save(where=model_table_names,
                                     data_lake=True,
                                     force=force,
                                     data_lake_container=data_lake_container)
                else:
                    self.model_.save(where=(schema, model_table_names), force=force)
            else:
                for i, table_name in enumerate(list(model_table_names)):
                    if storage_type == 'HDL':
                        self.model_[i].save(where=table_name,
                                            data_lake=True,
                                            force=force,
                                            data_lake_container=data_lake_container)
                    else:
                        self.model_[i].save(where=(schema, table_name), force=force)

    def _create_model_table(self, schema, table_name, col_names, attribute_name):
        """
        Creates the model table if it does not exists.
        The table is empty with a primary key on NAME, VERSION.

        Parameters
        ----------
        schema: str
            The schema name
        table_names: str
            The table name
        col_names: list of str
            The list of columns to put in the create table statement:
            create column table <table_name> as (select <col_names> from <artifact_table>).
        """
        if attribute_name != 'model_':
            raise ValueError('Unexpected model tables type', attribute_name, table_name)
        conn_context = getattr(self, 'conn_context')
        with conn_context.connection.cursor() as cursor:
            artifact_df = getattr(self, attribute_name, None)
            # Creates empty table
            sql = 'CREATE COLUMN TABLE {schema_name}.{table_name}'.format(
                schema_name=quotename(schema),
                table_name=quotename(table_name))
            sql = sql + ' AS (SELECT {COLS} FROM ({SOURCE}) where 1>2)'.format(
                SOURCE=artifact_df.select_statement,
                COLS=col_names
            )
            execute_logged(cursor, sql, conn_context.sql_tracer, conn_context)
            # Creates primary key
            sql = 'ALTER TABLE {schema_name}.{table_name}'.format(
                schema_name=quotename(schema),
                table_name=quotename(table_name))
            sql = sql + ' ADD CONSTRAINT {name} primary key(NAME, VERSION)'.format(
                name=quotename(table_name + '_PK'))
            execute_logged(cursor, sql, conn_context.sql_tracer, conn_context)

    def _load_model_tables(self, schema_name, model_table_names, name, version, conn_context=None): #pylint: disable=too-many-arguments
        """
        Copies the model content into a new artifact table for APL.
        This method must be implemented in a subclass.

        For PAL, it points the persisted model to model_ or pmml_/coefficient_ for glm and
         regression.
        """
        raise NotImplementedError("The method _load_model_tables is not implemented.")
