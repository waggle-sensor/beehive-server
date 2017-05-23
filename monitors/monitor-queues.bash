while true; do
    queuesTooFull=`docker exec beehive-rabbitmq bash -c "rabbitmqctl list_queues" | grep -v node_ | grep -v Listing | awk '($2 >= 80){print}' `
    if [ $(echo $queuesTooFull | wc -w) -ne 0 ]; then 
        /bin/slack-ops ":exclamation: :ocean: queue(s) filling up:\n\`\`\`\n${queuesTooFull}\n\`\`\`"
        sleep 300    # extra time - so we don't flood slack
    fi 
    sleep 30 
done
