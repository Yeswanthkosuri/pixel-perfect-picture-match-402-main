export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "14.18"
  }
  public: {
    Tables: {
      avatars: {
        Row: {
          appearance: Json
          consent_accepted_at: string | null
          consent_version: string | null
          created_at: string
          display_name: string
          generation_provider: string | null
          id: string
          model_url: string | null
          owner_id: string
          photo_path: string | null
          preview_url: string | null
          rig_id: string | null
          status: string
          updated_at: string
        }
        Insert: {
          appearance?: Json
          consent_accepted_at?: string | null
          consent_version?: string | null
          created_at?: string
          display_name?: string
          generation_provider?: string | null
          id?: string
          model_url?: string | null
          owner_id: string
          photo_path?: string | null
          preview_url?: string | null
          rig_id?: string | null
          status?: string
          updated_at?: string
        }
        Update: {
          appearance?: Json
          consent_accepted_at?: string | null
          consent_version?: string | null
          created_at?: string
          display_name?: string
          generation_provider?: string | null
          id?: string
          model_url?: string | null
          owner_id?: string
          photo_path?: string | null
          preview_url?: string | null
          rig_id?: string | null
          status?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "avatars_owner_id_fkey"
            columns: ["owner_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
        ]
      }
      loadouts: {
        Row: {
          abilities: string[]
          appearance: Json
          avatar_id: string | null
          created_at: string
          elements: string[]
          id: string
          is_active: boolean
          name: string
          owner_id: string
          updated_at: string
          weapon_id: string
        }
        Insert: {
          abilities?: string[]
          appearance?: Json
          avatar_id?: string | null
          created_at?: string
          elements?: string[]
          id?: string
          is_active?: boolean
          name: string
          owner_id: string
          updated_at?: string
          weapon_id?: string
        }
        Update: {
          abilities?: string[]
          appearance?: Json
          avatar_id?: string | null
          created_at?: string
          elements?: string[]
          id?: string
          is_active?: boolean
          name?: string
          owner_id?: string
          updated_at?: string
          weapon_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "loadouts_avatar_id_fkey"
            columns: ["avatar_id"]
            isOneToOne: false
            referencedRelation: "avatars"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "loadouts_owner_id_fkey"
            columns: ["owner_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
        ]
      }
      profiles: {
        Row: {
          avatar_url: string | null
          created_at: string
          display_name: string
          id: string
          updated_at: string
          username: string
        }
        Insert: {
          avatar_url?: string | null
          created_at?: string
          display_name?: string
          id: string
          updated_at?: string
          username: string
        }
        Update: {
          avatar_url?: string | null
          created_at?: string
          display_name?: string
          id?: string
          updated_at?: string
          username?: string
        }
        Relationships: []
      }
      worlds: {
        Row: {
          allowed_abilities: string[]
          allowed_elements: string[]
          allowed_weapons: string[]
          created_at: string
          description: string
          duration_minutes: number
          friendly_fire: boolean
          game_mode: string
          id: string
          map_id: string
          max_players: number
          name: string
          owner_id: string
          respawn: string
          settings: Json
          status: string
          story_background: string
          story_dialogue: string
          story_mission: string
          story_objective: string
          story_title: string
          story_win_condition: string
          thumbnail_url: string | null
          updated_at: string
          visibility: string
        }
        Insert: {
          allowed_abilities?: string[]
          allowed_elements?: string[]
          allowed_weapons?: string[]
          created_at?: string
          description?: string
          duration_minutes?: number
          friendly_fire?: boolean
          game_mode?: string
          id?: string
          map_id?: string
          max_players?: number
          name: string
          owner_id: string
          respawn?: string
          settings?: Json
          status?: string
          story_background?: string
          story_dialogue?: string
          story_mission?: string
          story_objective?: string
          story_title?: string
          story_win_condition?: string
          thumbnail_url?: string | null
          updated_at?: string
          visibility?: string
        }
        Update: {
          allowed_abilities?: string[]
          allowed_elements?: string[]
          allowed_weapons?: string[]
          created_at?: string
          description?: string
          duration_minutes?: number
          friendly_fire?: boolean
          game_mode?: string
          id?: string
          map_id?: string
          max_players?: number
          name?: string
          owner_id?: string
          respawn?: string
          settings?: Json
          status?: string
          story_background?: string
          story_dialogue?: string
          story_mission?: string
          story_objective?: string
          story_title?: string
          story_win_condition?: string
          thumbnail_url?: string | null
          updated_at?: string
          visibility?: string
        }
        Relationships: [
          {
            foreignKeyName: "worlds_owner_id_fkey"
            columns: ["owner_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends (DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never) = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends (DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never) = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends (DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never) = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends (DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never) = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends (PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never) = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {},
  },
} as const
