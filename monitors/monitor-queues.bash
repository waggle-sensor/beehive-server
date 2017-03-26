while true; do
    queuesNonEmpty=`docker exec beehive-rabbitmq bash -c "rabbitmqctl list_queues" | grep -v node_ | grep -v Listing | awk '($2 >= 20){print}' `
    echo $queuesNonEmpty
    if [ $(echo $queuesNonEmpty | wc -l) -ne 0 ]; then 
        /bin/slack-ops ":exclamation: :ocean: queue(s) filling up:\n\`\`\`\n${queuesNonEmpty}\n\`\`\`"
        sleep 60
    fi 
    sleep 60 
done

