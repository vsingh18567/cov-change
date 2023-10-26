poetry install
poetry build

for i in dist/*.whl
do
    pip3 install $i --force-reinstall;
    break;
done
