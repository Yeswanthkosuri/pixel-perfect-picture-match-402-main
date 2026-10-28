-- ELEMENTAL ARENA foundation schema

-- 1. Player profiles (1:1 with auth users)
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  username text unique not null,
  display_name text not null default '',
  avatar_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

grant select, update on public.profiles to authenticated;
grant select on public.profiles to anon;
grant all on public.profiles to service_role;

alter table public.profiles enable row level security;

create policy "Users can view their own profile"
  on public.profiles for select to authenticated
  using (auth.uid() = id);

create policy "Public read of profile handles"
  on public.profiles for select to anon
  using (true);

create policy "Users can update their own profile"
  on public.profiles for update to authenticated
  using (auth.uid() = id)
  with check (auth.uid() = id);

-- 2. Avatar records (photo + generated model references)
create table public.avatars (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references public.profiles(id) on delete cascade,
  display_name text not null default '',
  status text not null default 'none' check (status in ('none','pending','ready','failed')),
  generation_provider text,
  photo_path text,
  model_url text,
  preview_url text,
  rig_id text,
  appearance jsonb not null default '{}'::jsonb,
  consent_version text,
  consent_accepted_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (owner_id, display_name)
);

grant select, insert, update, delete on public.avatars to authenticated;
grant all on public.avatars to service_role;

alter table public.avatars enable row level security;

create policy "Owners manage their avatars"
  on public.avatars for all to authenticated
  using (auth.uid() = owner_id)
  with check (auth.uid() = owner_id);

-- 3. Character loadouts (two elements, five abilities, one weapon)
create table public.loadouts (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references public.profiles(id) on delete cascade,
  name text not null,
  elements text[] not null default '{}'::text[] check (coalesce(array_length(elements, 1), 0) = 2),
  abilities text[] not null default '{}'::text[] check (coalesce(array_length(abilities, 1), 0) = 5),
  weapon_id text not null default '',
  appearance jsonb not null default '{}'::jsonb,
  avatar_id uuid references public.avatars(id) on delete set null,
  is_active boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (owner_id, name)
);

create index loadouts_owner_idx on public.loadouts (owner_id);

grant select, insert, update, delete on public.loadouts to authenticated;
grant all on public.loadouts to service_role;

alter table public.loadouts enable row level security;

create policy "Owners manage their loadouts"
  on public.loadouts for all to authenticated
  using (auth.uid() = owner_id)
  with check (auth.uid() = owner_id);

-- 4. Custom worlds (drafts are private; published public listings are browsable)
create table public.worlds (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references public.profiles(id) on delete cascade,
  name text not null,
  description text not null default '',
  map_id text not null default '',
  game_mode text not null default 'free_for_all',
  max_players integer not null default 8,
  duration_minutes integer not null default 10,
  respawn text not null default 'instant',
  friendly_fire boolean not null default false,
  visibility text not null default 'private' check (visibility in ('private','public')),
  status text not null default 'draft' check (status in ('draft','published')),
  story_title text not null default '',
  story_background text not null default '',
  story_objective text not null default '',
  story_mission text not null default '',
  story_win_condition text not null default '',
  story_dialogue text not null default '',
  allowed_elements text[] not null default '{}'::text[],
  allowed_abilities text[] not null default '{}'::text[],
  allowed_weapons text[] not null default '{}'::text[],
  thumbnail_url text,
  settings jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index worlds_owner_idx on public.worlds (owner_id);
create index worlds_public_idx on public.worlds (status, visibility) where status = 'published' and visibility = 'public';

grant select, insert, update, delete on public.worlds to authenticated;
grant select on public.worlds to anon;
grant all on public.worlds to service_role;

alter table public.worlds enable row level security;

create policy "Owners manage their worlds"
  on public.worlds for all to authenticated
  using (auth.uid() = owner_id)
  with check (auth.uid() = owner_id);

create policy "Anyone can view published public worlds"
  on public.worlds for select to anon
  using (status = 'published' and visibility = 'public');

-- 5. updated_at maintenance
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger profiles_set_updated_at
  before update on public.profiles
  for each row execute function public.set_updated_at();

create trigger avatars_set_updated_at
  before update on public.avatars
  for each row execute function public.set_updated_at();

create trigger loadouts_set_updated_at
  before update on public.loadouts
  for each row execute function public.set_updated_at();

create trigger worlds_set_updated_at
  before update on public.worlds
  for each row execute function public.set_updated_at();

-- 6. Auto-create a profile on signup (Auth lifecycle exception)
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  base text;
  candidate text;
  suffix int := 0;
begin
  base := lower(regexp_replace(coalesce(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1), 'player'), '[^a-z0-9_]', '', 'g'));
  if base is null or length(base) < 3 then
    base := 'player';
  end if;
  candidate := base;
  while exists (select 1 from public.profiles p where p.username = candidate) loop
    suffix := suffix + 1;
    candidate := base || suffix::text;
  end loop;
  insert into public.profiles (id, username, display_name)
  values (
    new.id,
    candidate,
    coalesce(new.raw_user_meta_data->>'display_name', candidate)
  );
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
