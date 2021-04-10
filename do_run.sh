while :; do
    python3 kv_server.py > 1.out 2> /dev/null
    cat 1.out >> 1.out.total
    cat 1.err >> 1.err.total
done

