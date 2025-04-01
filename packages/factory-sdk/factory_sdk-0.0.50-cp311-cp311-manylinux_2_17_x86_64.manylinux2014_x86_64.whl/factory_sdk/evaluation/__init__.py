from factory_sdk.dto.adapter import AdapterObject
from factory_sdk.dto.dataset import DatasetObject
from factory_sdk.dto.recipe import RecipeObject, RecipeRevision
from factory_sdk.recipe import download_recipe
from factory_sdk.models import download_model
from factory_sdk.datasets import download_dataset
from factory_sdk.adapters import download_adapter
from factory_sdk.eval.start import start_eval
from factory_sdk.dto.evaluation import EvalArgs



class Evaluation:
    def __init__(self,client):
        self.client=client
        self._name=None
        self._adapters=[]
        self._metrics=[]
        self._recipe=None
        self._eval_args=EvalArgs()

    def with_name(self,name):
        self._name=name
        return self
    
    def for_adapter(self,adapter:AdapterObject):
        assert adapter!=None,"adapter must be provided"
        assert isinstance(adapter,AdapterObject),"adapter must be an instance of AdapterObject"
        
        self._adapters.append(adapter)
        return self

    def using_metric(self,metric,**kwargs): # have to be a callable
        assert callable(metric),"metric must be callable"
        self._metrics.append((
            metric,
            kwargs
        ))

        return self

    def on_recipe(self,recipe:RecipeObject):
        assert recipe!=None,"recipe must be provided"
        assert isinstance(recipe,RecipeObject),"recipe must be an instance of RecipeObject"
        self._recipe=recipe

        return self
    
    def with_config(self,eval_args:EvalArgs):
        assert eval_args!=None,"eval_args must be provided"
        assert isinstance(eval_args,EvalArgs),"eval_args must be an instance of EvalArgs"
        self._eval_args=eval_args

        return self
    
    def eval(self):

        recipe_revision: RecipeRevision = self._recipe.get_revision()
        
        dataset_ref = None
        for dep in recipe_revision.dependencies:
            if dep.type == "dataset":
                dataset_ref = dep
                break
        assert dataset_ref is not None, "Dataset not found in recipe dependencies"

        #### Download the dataset and recipe ####

        dataset_path = download_dataset(
            dataset_ref.id, dataset_ref.revision, self.client, return_path=True
        )

        recipe_path = download_recipe(
            self._recipe.meta.id, recipe_revision.id, self.client, return_path=True
        )

        def get_model(adapter):
            model_ref = None
            adapter_ref = adapter.get_revision()
            for dep in adapter_ref.dependencies:
                if dep.type == "model":
                    model_ref = dep
                    break
            assert model_ref is not None, "Model not found in adapter dependencies"
            return model_ref

        adapter_paths=[
            {
                "path":download_adapter(
                    adapter.meta.id, adapter.revision, self.client, return_path=True
                ),
                "id":adapter.meta.id,
                "revision":adapter.revision,
                "model":{ "id":get_model(adapter).id, "revision":get_model(adapter).revision }
            }
            for adapter in self._adapters
        ]

        model_id_revisions=[]
        models=[]
        for adapter in self._adapters:
            adapter_ref = adapter.get_revision()
            model_ref = get_model(adapter)
            
            midref=model_ref.id+"#"+model_ref.revision
            if midref not in model_id_revisions:
                model_id_revisions.append(midref)
                models.append(
                    {
                        "path":download_model(
                            model_ref.id, model_ref.revision, self.client, return_path=True
                        ),
                        "id":model_ref.id,
                        "revision":model_ref.revision
                    }
                )



        start_eval(
            eval_args=self._eval_args,
            model_paths=models,
            adapter_paths=adapter_paths,
            dataset_path=dataset_path,
            recipe_path=recipe_path,
            client_params=self.client.get_init_params(),
            eval_name=self._name,
        )

