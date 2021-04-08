while :; do
    python3 kv_server.py > 1.out 2> 1.err
    cat 1.out >> 1.out.total
    cat 1.err >> 1.err.total
done

