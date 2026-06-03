# -*- coding: utf-8 -*-
"""Eight Diagrams Numerology Therapy — English CLI Launcher"""
from xiangshu_data_en import RECIPES as DATA

def search(keyword):
    k = keyword.lower()
    return [r for r in DATA if any(k in s.lower() for s in r['symptoms'])]

def main():
    all_syms = len({s for r in DATA for s in r['symptoms']})
    print()
    print('=== Eight Diagrams Numerology Therapy ===')
    print('  %d recipes | %d symptoms' % (len(DATA), all_syms))
    print()
    print('Commands: search <keyword> | list | quit')
    while True:
        try:
            line = input('>>> ').strip()
        except EOFError:
            break
        if not line:
            continue
        parts = line.split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ''
        if cmd in ('q', 'quit', 'exit'):
            break
        elif cmd == 'list':
            for i, r in enumerate(DATA[:20], 1):
                print('%d. %s | %s' % (i, r['formula'], r['symptoms'][0]))
            print('... (%d total)' % len(DATA))
        elif cmd == 'search':
            if not arg:
                print('Usage: search <keyword>')
                continue
            results = search(arg)
            if not results:
                print('No results.')
            else:
                for r in results:
                    print('  Formula: %s' % r['formula'])
                    print('  Symptoms: %s' % ', '.join(r['symptoms']))
                    print('  Explanation: %s' % r['explanation'])
                    print()
        else:
            results = search(line)
            if not results:
                print('Not found. Try: search <keyword>')
            else:
                for r in results:
                    print('  %s | %s' % (r['formula'], ', '.join(r['symptoms'][:3])))

if __name__ == '__main__':
    main()
