COUNTER=0
while [  $COUNTER -lt 1000 ]; do
  cp trash-recycling-pickup.yaml trash-recycling-pickup-$COUNTER.yaml
  gsed -i "1cslug: trash-recycling-pickup-$COUNTER" trash-recycling-pickup-$COUNTER.yaml
  gsed -i "7ctitle_en: blarg$COUNTER" trash-recycling-pickup-$COUNTER.yaml
  let COUNTER=COUNTER+1 
done
