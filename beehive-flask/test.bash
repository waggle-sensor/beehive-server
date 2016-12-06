
function url() {
	echo " "
	echo "#############" $*
	echo " "
	curl $*
	echo " "
}


if false
then
	url 0.0.0.0/admin/
	url 0.0.0.0/admin/search/

	url 0.0.0.0/api/
	url 0.0.0.0/api/1/
	url 0.0.0.0/api/1/epoch
	url 0.0.0.0/api/1/nodes/
	url 0.0.0.0/api/1/nodes/0000001e061088c8/dates/
	url 0.0.0.0/api/nodes/0000001e061088c8/dates/
	url 0.0.0.0/api/1/nodes_last_update/
	url 0.0.0.0/api/1/WCC_node/0000001e061088c8/
fi

url 0.0.0.0/
url 0.0.0.0/wcc/test/
url "0.0.0.0/wcc/test/?dog=cat&tiger=lion"
url 0.0.0.0/web/
url 0.0.0.0/web/wcc/test/
url "0.0.0.0/web/wcc/test/?dog=cat&tiger=lion"
url 0.0.0.0/web/wcc/
# url 0.0.0.0/web/wcc/node/0000001e061088c8
echo " "

