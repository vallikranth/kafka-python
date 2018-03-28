'''
Created on Mar 27, 2018

@author: vallikranth
'''

from confluent_kafka import Producer
import logging


if __name__ == '__main__':
    logger = logging.getLogger('consumer')
    logger.setLevel(logging.INFO)
    
    #handler = TimedRotatingFileHandler('/tmp/consumer.log',when='midnight', backupCount=2)
    handler = logging.StreamHandler();
    handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(name)s - %(message)s','%Y-%m-%d %H:%M:%S'))
    logger.addHandler(handler)
    
    config={'bootstrap.servers': 'localhost:9092',
            'session.timeout.ms': 6000
    }
    
    sampleProducer = Producer(config)

    for data in range(10):
        sampleProducer.produce('test', 'Msg:'+str(data), str(data))
        logger.info('sent event with Key:%s ',data)
    
    sampleProducer.flush()