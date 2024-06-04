import sys

def progress_bar(count, total, prefix='', suffix='', length=50, fill='█'):
    progress = count / total
    filled_length = int(length * progress)
    bar = fill * filled_length + '-' * (length - filled_length)
    percent = ("{0:.1f}").format(progress * 100)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    sys.stdout.flush()