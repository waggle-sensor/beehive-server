MAX_NUM_MESSAGES=20
while true; do
    queuesTooFull=`docker exec beehive-rabbitmq bash -c "rabbitmqctl list_queues" | grep -v node_ | grep -v Listing | awk '($2 >= $MAX_NUM_MESSAGES){print}' `
    echo $queuesTooFull
    if [ $(echo $queuesTooFull | wc -l) -ne 0 ]; then 
        /bin/slack-ops ":exclamation: :ocean: queue(s) filling up:\n\`\`\`\n${queuesTooFull}\n\`\`\`"
        sleep 600    # extra time - so we don't flood slack
    fi 
    sleep 60 
done

