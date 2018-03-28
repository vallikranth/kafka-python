'''
Created on Mar 24, 2018

@author: 
'''

from confluent_kafka import Consumer, KafkaException, KafkaError
import logging
import sys
#import os.path
#sys.path.append(os.path.join(__file__), '../../../')
#from logging.handlers import TimedRotatingFileHandler



if __name__ == '__main__':
    #Add logger
    logger = logging.getLogger('consumer')
    logger.setLevel(logging.INFO)
    
    #handler = TimedRotatingFileHandler('/tmp/consumer.log',when='midnight', backupCount=2)
    handler = logging.StreamHandler();
    handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(name)s - %(message)s','%Y-%m-%d %H:%M:%S'))
    logger.addHandler(handler)
    
    config={'bootstrap.servers': 'localhost:9092',
            'group.id': 'python-consumer', 
            'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'}
    }
    
    topics = ['test']
    sampleConsumer = Consumer(config)
    sampleConsumer.subscribe(topics)
    
    try:
        while True:
            msg = sampleConsumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    #===========================================================
                    # sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                    #                  (msg.topic(), msg.partition(), msg.offset()))
                    #===========================================================
                    logger.info('End of partition. Topic:%s, partition:%s, offset:%s', msg.topic(), msg.partition(), msg.offset())
                elif msg.error():
                    # Error
                    raise KafkaException(msg.error())
            else:
                # Proper message
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
                #print(msg.value())
                logger.debug('read message at offset:%s with key:%s from topic:%s', msg.offset(),str(msg.key()),msg.topic())
                logger.info('Key:%s Value:%s',str(msg.key().decode('utf8')),str(msg.value().decode('utf8')))

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')
    
    finally:
        sampleConsumer.close()
        