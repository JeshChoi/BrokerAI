'use client'

import { useQuery } from 'convex/react';
import { api } from '@/../convex/_generated/api';

export default function Home() {

  const halls = useQuery(api.findings.get);

  return (
    <main class="flex flex-col justify-center items-center min-h-screen w-full">
      {
        halls == undefined ? <span>Loading...</span> :
          halls.map(({ _id, _creationTime, name }) => {
            return (
              <span id={_id} class="flex gap-4 border">
                <span>{(new Date(_creationTime)).toLocaleTimeString()}</span>
                <span>{name}</span>
              </span>
            )
          })
      }
    </main>
  );
}