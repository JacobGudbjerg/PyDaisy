# pydaisy
pydaisy provides various tools to read, write and manipulate [Daisy](https://daisy.ku.dk) input- and outputfiles.

# Usage
.dai-files:
```sh
from pydaisy.Daisy import *
d = DaisyModel(r'C:\Program Files\Daisy 5.72\exercises\Exercise01.dai')
print(d.starttime)
dry_bulk_density = d.Input['defhorizon'][0]['dry_bulk_density'].getvalue()
d.Input['defhorizon'][0]['dry_bulk_density'].setvalue(1.1*dry_bulk_density)
d.save_as(r'C:\Program Files\Daisy 5.72\exercises\Exercise01_new.dai')
d.daisyexecutable = r'C:\Program Files\Daisy 5.72\bin\Daisy.exe'
d.run()
```

.dlf- and .dwf-files:
```sh
from datetime import datetime
from pydaisy.Daisy import *
dlf = DaisyDlf(r'C:\Program Files\Daisy 5.72\exercises\Taastrup6201.dwf')
pandasdata = dlf.Data
numpy_data = dlf.numpydata
i=dlf.get_index(datetime(1962,4,14))
pandasdata['Precip'][i]=10
dlf.save(r'C:\Program Files\Daisy 5.72\exercises\Taastrup6201_saved.dwf')
```


Parallel runs:
```sh
from pydaisy.Daisy import *
daisyfiles =[r'c:\daisy\model1\setup.dai', r'c:\daisy\model2\setup.dai', r'c:\daisy\model3\setup.dai']
run_many(daisyfiles, NumberOfProcesses=3)
```
The code above will run the three daisy-simulations in parallel.
