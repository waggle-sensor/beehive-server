function url() {
    echo " "
    echo "#############" $*
    echo " "
    curl $*
    echo " "
}


if true; then
    url 0.0.0.0/admin/
    url 0.0.0.0/admin/search/

    url 0.0.0.0/api/
    url 0.0.0.0/api/1/
    url 0.0.0.0/api/1/epoch
    url 0.0.0.0/api/1/nodes/
    url 0.0.0.0/api/1/nodes/?all=true
    url 0.0.0.0/api/nodes
    url 0.0.0.0/api/1/nodes/ffffffffffff0001/dates/?version=2
    url 0.0.0.0/api/nodes/ffffffffffff0001/dates/
    url 0.0.0.0/api/1/nodes_last_update/
    url 0.0.0.0/api/1/nodes/ffffffffffff0001/export
    url 0.0.0.0/api/1/WCC_node/ffffffffffff0001/
fi

if false; then
    url 0.0.0.0/
    url 0.0.0.0/wcc/test/
    url "0.0.0.0/wcc/test/?dog=cat&tiger=lion"
    url 0.0.0.0/wcc/
    url 0.0.0.0/web/wcc/node/ffffffffffff0001
fi
echo " "
