BASEDIR=$(dirname $0)
cd "${BASEDIR}"

/home/admin/rpip wheel --no-build-isolation --no-deps -w build .

#mkdir ../whl
mv ./build/*.whl ../whl/

rm -R ./build/lib
rm -R ./build/bdist.*
rm -R *.egg-info