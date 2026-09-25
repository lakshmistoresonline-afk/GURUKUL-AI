import englishConfig from '../presentation-config/english.json';
import mathConfig from '../presentation-config/mathematics.json';
import genericConfig from '../presentation-config/generic.json';

export interface ContentManifestItem {
  type: string;
  sourceType?: string;
  count: number;
  renderer: string;
}

export interface ContentManifest {
  chapterId: string;
  contentTypes: ContentManifestItem[];
}

export interface NavigationTab {
  id: string;
  label: string;
  order: number;
  contentTypes: string[];
}

const CONFIG_MAP: Record<string, any> = {
  english: englishConfig,
  mathematics: mathConfig,
  generic: genericConfig,
};

export class NavigationBuilder {
  /**
   * Dynamically constructs available navigation tabs for a chapter.
   * Sorts tabs strictly by explicit presentation order (Quiz always last: order 60).
   * ZERO EMPTY PLACEHOLDERS RULE:
   * Only tabs that contain at least one available content type in the manifest are returned.
   */
  static buildNavigation(subject: string, manifest: ContentManifest): NavigationTab[] {
    const subjectKey = subject.toLowerCase();
    const config = CONFIG_MAP[subjectKey] || CONFIG_MAP['generic'];
    const presentTypes = new Set<string>();

    for (const item of manifest.contentTypes) {
      presentTypes.add(item.type);
      if (item.sourceType) {
        presentTypes.add(item.sourceType);
      }
    }

    const activeTabs: NavigationTab[] = [];
    const sortedGroups = [...config.groups].sort((a, b) => (a.order || 999) - (b.order || 999));

    for (const group of sortedGroups) {
      if (group.contentTypes.includes('*')) {
        if (presentTypes.size > 0) {
          activeTabs.push({
            id: group.id,
            label: group.label,
            order: group.order || 999,
            contentTypes: Array.from(presentTypes),
          });
        }
      } else {
        const matchingTypes = group.contentTypes.filter((t: string) => presentTypes.has(t));
        if (matchingTypes.length > 0) {
          activeTabs.push({
            id: group.id,
            label: group.label,
            order: group.order || 999,
            contentTypes: matchingTypes,
          });
        }
      }
    }

    return activeTabs;
  }
}
