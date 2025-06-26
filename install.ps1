$Env:PIP_DISABLE_PIP_VERSION_CHECK = 1
$Env:PIP_NO_CACHE_DIR = 1

function InstallFail {
    Write-Output "install failed"
    Read-Host | Out-Null ;
    Exit
}


function Check {
    param (
        $ErrorInfo
    )
    if (!($?)) {
        Write-Output $ErrorInfo
        InstallFail
    }
}


if (!(Test-Path -Path "venv")) {
    Write-Output "creating venv..."
    python -m venv venv
    Check "Failed to create a virtual environment. Please check whether python is installed and whether the python version is the 64-bit version of python 3.10, or whether the python directory is in the environment variable PATH."
}


.\venv\Scripts\activate
Check "activate venv failed"

pip install pyelftools==0.29 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pdf2docx==0.5.6 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install scheduler==0.8.8 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install colorlog==6.9.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install PyYAML
pip install fastapi
pip install paddleocr
pip install paddlepaddle
pip install uvicorn
pip install croniter
pip install psutil
pip install plyer
pip install uiautomator2
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

Write-Output "install complete"
Read-Host | Out-Null ;
