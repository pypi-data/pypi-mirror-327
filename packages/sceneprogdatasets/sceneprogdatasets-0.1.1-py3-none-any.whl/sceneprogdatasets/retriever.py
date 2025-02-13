from .HSSD.hssd import AssetRetrieverHSSD
from .future.future import AssetRetrieverFuture

class SceneProgAssetRetriever:
    def __init__(self):
       
        import os
        from pathlib import Path
        path = Path(__file__).parent
        if not os.path.exists(os.path.join(path,'HSSD/assets/model2description.json')):
            os.makedirs(os.path.join(path,'HSSD/assets'))
            os.makedirs(os.path.join(path,'future/assets'))
            os.system(f"aws s3 cp s3://sceneprog-nautilus/sceneprogdatasets/future/ {os.path.join(path,'future/assets')} --recursive")
            os.system(f"aws s3 cp s3://sceneprog-nautilus/sceneprogdatasets/hssd/ {os.path.join(path,'HSSD/assets')} --recursive")
            # os.system(f'bash {path}/download.sh')
        
        self.hssd = AssetRetrieverHSSD()
        self.future = AssetRetrieverFuture()
    
    def __call__(self, description):
        ## first search in Future
        future_results = self.future.run(description)
        if not future_results == 'No models found':
            return ("FUTURE",future_results)
        
        ## then search in HSSD
        hssd_results = self.hssd.run(description)
        if not hssd_results == 'No models found':
            return ("HSSD",hssd_results)
        
        return "No models found"