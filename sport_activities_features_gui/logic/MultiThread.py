from sport_activities_features.tcx_manipulation import TCXFile
import pandas as pd
from multiprocessing import Pool, Manager
#Vito, Nejc, Nejc vam zelijo vesele SVETKE 2006 
class MultiThread:  
    def single_load(self, path_of_file: str) -> pd.DataFrame: 
        try:
            tcx_file = TCXFile()
            activity = tcx_file.read_one_file(path_of_file)
            integral_metrics = tcx_file.extract_integral_metrics(path_of_file)
            all_data= activity | integral_metrics
            df = pd.DataFrame(all_data)
            return df
        except:
            return pd.DataFrame

    def _single_load_inner(self, path_of_file: str, data): 
        try:
            tcx_file = TCXFile()
            activity = tcx_file.read_one_file(path_of_file)
            integral_metrics = tcx_file.extract_integral_metrics(path_of_file)
            all_data= activity | integral_metrics
            data.append(all_data)
        except Exception as e:
            print(str(e)+'\nfile at path '+path_of_file+'\nwas not read')
            
    
    def bulk_load(self, files: list, num_of_processes: int) -> dict:
        with Manager() as manager:
            data = manager.list()
            with Pool(processes=num_of_processes) as pool:
                pool.starmap(self._single_load_inner, [(file, data) for file in files])               
            return {
                'data' : pd.DataFrame(list(data)),
                'numOfFiles': len(files),
                'numOfFilesNotRead' : (len(files) - len(data))
            }