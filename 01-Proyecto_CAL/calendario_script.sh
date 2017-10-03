echo "--------------------------------------------------------"
echo "Aplicación para la creación automática del horario UIB: "
echo "--------------------------------------------------------"
echo
echo "Será necesaria la instalación de recursos, una vez acabado el proceso,"
echo "pueden ser borrados"
echo
echo
echo
echo
echo
echo
echo
echo
pwd=$(pwd)
cd ./cal/cal/spiders/
scrapy crawl calendar -o horario1718.csv -t csv

echo "Scrapy terminado, modificando csv"
python cambio_titulo_csv.py

echo "----------------------------------------------------------------------"
echo "Se ha realizado correctamente la creación automática del horario UIB: "
echo "----------------------------------------------------------------------"

mv horario1718_modified.csv $pwd
echo "El csv correspondiente es el horario1718_modified.csv "
