"""Generate start/resume notebooks without editable run flags."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def cell(kind,text,i):
    c={'cell_type':kind,'id':f'dmnerf-{i}','metadata':{},'source':text.splitlines(keepends=True)}
    if kind=='code': c.update(execution_count=None,outputs=[])
    return c

def build(platform,resume):
    kaggle=platform=='Kaggle'; mode='Resume' if resume else 'Study'
    cells=[]
    def add(kind,text): cells.append(cell(kind,text,len(cells)))
    add('markdown',f'''# DM-NeRF / DM-SR — study ({platform}, {mode})
Ative GPU e Internet na interface e execute todas as células. Não edite código.
{'Na continuação, anexe em Add Input → Notebook Output a saída anterior deste projeto.' if kaggle and resume else ''}
{'Use Save Version → Save & Run All para preservar saídas.' if kaggle else 'Autorize o Google Drive quando solicitado. Checkpoints são gravados nele.'}
O início executa smoke test e piloto de até uma hora. A continuação retoma o treino até o orçamento da sessão.
Uma sessão gratuita não garante convergência. Somente study é executada; nenhuma decisão congelada é alterada.
''')
    setup='''from pathlib import Path
import json, shutil, subprocess, sys

def run(*args):
    subprocess.run([str(x) for x in args], check=True)

run('nvidia-smi')
'''
    if kaggle:
        setup+="BASE=Path('/kaggle/temp/dissertacao-dmnerf')\nOUTPUT=Path('/kaggle/working/dmnerf-results')\n"
    else:
        setup+="from google.colab import drive\ndrive.mount('/content/drive')\nBASE=Path('/content/dissertacao-dmnerf')\nOUTPUT=Path('/content/drive/MyDrive/dissertacao-dmnerf/dmnerf-results')\n"
    if resume and kaggle:
        setup+='''if not (OUTPUT/'raw/study/experiment/latest.tar').exists():
    candidates=[]
    for state in Path('/kaggle/input').rglob('training_state.json'):
        if state.parent.name=='experiment' and (state.parent/'identity.json').is_file() and (state.parent/'latest.tar').is_file():
            candidates.append((json.loads(state.read_text())['iteration'],state.parents[3]))
    if not candidates:
        raise RuntimeError('Anexe a saída do piloto/continuação em Add Input → Notebook Output.')
    previous=sorted(candidates,key=lambda item:(item[0],str(item[1])))[-1][1]
    shutil.copytree(previous,OUTPUT,dirs_exist_ok=True)
'''
    if resume:
        setup+="if not (OUTPUT/'raw/study/experiment/latest.tar').exists():\n    raise RuntimeError('Execute primeiro o notebook Study: checkpoint piloto ausente.')\n"
    setup+='''BASE.mkdir(parents=True,exist_ok=True)
REPO=BASE/'sdf-generator'
WORK=BASE/'work'
if not REPO.exists():
    run('git','clone','--branch','dissertacao-2026','--single-branch',
        'https://github.com/Jfsslemos/sdf-generator.git',REPO)
run('git','-C',REPO,'rev-parse','HEAD')
lock=['--lock',OUTPUT/'environment.freeze.txt'] if (OUTPUT/'environment.freeze.txt').exists() else []
run(sys.executable,REPO/'tools/dmnerf/bootstrap.py','--work',WORK,*lock)
PYTHON=WORK/'env/bin/python'
run(PYTHON,'-c','import torch; assert torch.cuda.is_available(), "Ative GPU"; print(torch.cuda.get_device_name(0))')
'''
    add('code',setup)
    add('code',"run(PYTHON,REPO/'tools/dmnerf/prepare.py','--work',WORK)\n")
    if resume:
        add('code',"run(PYTHON,REPO/'tools/dmnerf/run.py','--work',WORK,'--output',OUTPUT,'--profile','full')\n")
    else:
        add('code',"run(PYTHON,REPO/'tools/dmnerf/run.py','--work',WORK,'--output',OUTPUT,'--profile','smoke')\n")
        add('code',"run(PYTHON,REPO/'tools/dmnerf/run.py','--work',WORK,'--output',OUTPUT,'--profile','pilot','--stages','train')\n")
    add('code',"""print('Resultados:',OUTPUT)
for state in sorted(OUTPUT.rglob('training_state.json')):
    print(state.relative_to(OUTPUT),json.loads(state.read_text()))
print('Pacote:',OUTPUT.parent/(OUTPUT.name+'-bundle.zip'))
""")
    add('markdown','''## Continuação
Envie o pacote de resultados para revisar tempo/VRAM e decidir viabilidade. No Kaggle, preserve a versão e anexe sua saída ao notebook Resume. No Colab, use Resume com o mesmo Drive.
O smoke é diagnóstico. Avaliação completa e meshing 256³ só ocorrem ao completar o treino. Ausência de superfície é registrada, não corrigida por mudança arbitrária do limiar.
Veja `docs/GPU_RUNBOOK.md`.''')
    nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python'},'accelerator':'GPU'},'cells':cells}
    (ROOT/f'notebooks/DMNeRF_{platform}_{mode}.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
    for platform in ('Kaggle','Colab'):
        for resume in (False,True): build(platform,resume)
