import React from 'react';
import { Composition } from 'remotion';
import { Video } from './Video';
import { FPS, T } from './theme';
import { TOTAL } from './data';
export const Root: React.FC = () => (
  <Composition id="StoryVideo" component={Video} durationInFrames={T(TOTAL)} fps={FPS} width={1080} height={1920} />
);
