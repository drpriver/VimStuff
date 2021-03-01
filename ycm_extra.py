def Settings(**kwargs):
    if kwargs['language'] == 'cfamily':
        return {
            'flags': ['-x', 'c', 'std=gnu17']
            }

