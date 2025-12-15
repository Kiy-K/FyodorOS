import React, { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

export interface StreamEvent {
  id: number;
  type: 'text' | 'json' | 'code';
  content: any;
  timestamp: string;
}

interface AgentStreamProps {
  events: StreamEvent[];
}

// A simple recursive component for the "Object Inspector"
const JsonNode: React.FC<{ data: any; label?: string; level?: number }> = ({ data, label, level = 0 }) => {
  const [expanded, setExpanded] = React.useState(level < 2);
  const isObject = typeof data === 'object' && data !== null;
  const isArray = Array.isArray(data);
  const isEmpty = isObject && Object.keys(data).length === 0;

  if (!isObject) {
    let valueColor = "text-yellow-300"; // String
    if (typeof data === 'number') valueColor = "text-blue-300";
    if (typeof data === 'boolean') valueColor = "text-purple-300";

    return (
      <div className="font-mono text-xs pl-4 hover:bg-zinc-900/50 flex">
        {label && <span className="text-zinc-500 mr-2 min-w-[60px]">{label}:</span>}
        <span className={`${valueColor} break-all`}>{JSON.stringify(data)}</span>
      </div>
    );
  }

  return (
    <div className="font-mono text-xs pl-2">
      <div
        className="flex items-center cursor-pointer hover:bg-zinc-900/50 py-0.5"
        onClick={() => setExpanded(!expanded)}
      >
        <span className="text-zinc-500 mr-1 w-3 inline-block text-center select-none">
            {isEmpty ? '' : (expanded ? '▼' : '▶')}
        </span>
        {label && <span className="text-zinc-400 mr-2">{label}:</span>}
        <span className="text-zinc-600 select-none">
            {isArray ? `Array(${data.length})` : `Object {${Object.keys(data).length}}`}
        </span>
      </div>

      {expanded && !isEmpty && (
        <div className="border-l border-zinc-800 ml-1.5">
          {Object.entries(data).map(([key, val]) => (
            <JsonNode key={key} label={key} data={val} level={level + 1} />
          ))}
        </div>
      )}
    </div>
  );
};

export const AgentStream: React.FC<AgentStreamProps> = ({ events }) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll
  useEffect(() => {
    if (scrollRef.current) {
        scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events]);

  return (
    <div
        className="flex-1 overflow-y-auto p-4 space-y-6 bg-background custom-scrollbar"
        ref={scrollRef}
        role="log"
        aria-live="polite"
    >
       {events.length === 0 && (
         <div className="text-muted text-center mt-20 font-mono text-sm opacity-50">
           SYSTEM READY. WAITING FOR INPUT...
         </div>
       )}

       {events.map((event) => (
         <div key={event.id} className="animate-in fade-in slide-in-from-bottom-2 duration-300">
            {/* Timestamp & Type Badge */}
            <div className="flex items-center space-x-2 mb-1 opacity-50">
                <span className="text-[10px] font-mono text-muted">{event.timestamp}</span>
                <span className="text-[9px] font-bold font-mono px-1 border border-zinc-700 rounded text-zinc-400 uppercase">
                    {event.type}
                </span>
            </div>

            {/* Content Block */}
            <div className="pl-2 border-l-2 border-zinc-800">

                {/* JSON RENDERER */}
                {event.type === 'json' && (
                    <div className="bg-surface border border-border p-2 rounded-sm overflow-x-auto">
                        <JsonNode data={event.content} />
                    </div>
                )}

                {/* TEXT / MARKDOWN RENDERER */}
                {event.type === 'text' && (
                    <div className="prose prose-invert prose-sm max-w-none prose-p:my-1 prose-headings:text-zinc-200 prose-pre:bg-surface prose-pre:border prose-pre:border-border">
                        <ReactMarkdown
                            components={{
                                code(props) {
                                    const {children, className, node, ...rest} = props
                                    const match = /language-(\w+)/.exec(className || '')
                                    return match ? (
                                        // @ts-ignore
                                        <SyntaxHighlighter
                                            {...rest}
                                            PreTag="div"
                                            children={String(children).replace(/\n$/, '')}
                                            language={match[1]}
                                            style={vscDarkPlus}
                                            customStyle={{ background: '#18181b', margin: 0 }}
                                        />
                                    ) : (
                                        <code {...rest} className={className}>
                                            {children}
                                        </code>
                                    )
                                }
                            }}
                        >
                            {event.content}
                        </ReactMarkdown>
                    </div>
                )}
            </div>
         </div>
       ))}
    </div>
  );
};
