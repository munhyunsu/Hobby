import main(_):
    print('Parsed args {0}'.format(FLAGS))
    print('Unparsed args {0}'.format(_))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()    
    FLAGS, _ = parser.parse_known_args()

    main(_)

