import numpy as np

import bentoml
from bentoml.io import JSON, NumpyNdarray

model_ref = bentoml.xgboost.get("ore_impurity_model:latest")

model_runner = model_ref.to_runner()

svc = bentoml.Service("ore_impurity_predictor", runners=[model_runner])


@svc.api(input=NumpyNdarray(), output=JSON())
def predict(application_data):
    prediction = model_runner.predict.run([application_data])
    print(prediction)
    result = np.expm1(prediction[0])
    return {"impurity": result}
